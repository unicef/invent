<template>
  <div class="LandingInitiativesTable">
    <el-table
      :data="initiativesTableData"
      :highlight-current-row="false"
      max-height="600"
      :lazy="true"
      stripe
      :empty-text="$gettext('No initiatives available') | translate"
    >
      <el-table-column
        v-for="({ name, id, count }, index) in omitedPhasesCount"
        :prop="name"
        :key="id"
        min-width="180"
        :fixed="index === 0 ? true : false"
      >
        <template slot="header" slot-scope="scope">
          <div id="header">
            <p id="header-title">{{ $gettext(name) | translate }}</p>
            <p id="header-count">{{ count }}</p>
          </div>
        </template>
        <template slot-scope="scope">
          <div v-if="index === 0">
            <p>{{ scope.row.sector.sector_name }}</p>
          </div>
          <div v-else>
            <nuxt-link
              :to="
                localePath({
                  name: 'organisation-initiatives-id-published',
                  params: { ...$route.params, id: card.id },
                })
              "
              v-for="card in scope.row[id]"
              :key="card.id"
              :class="card.stale ? 'link-card stale' : 'link-card'"
            >
              <div class="list-group-card">
                <div class="icon-div">
                  <i class="el-icon-time"></i>
                </div>
                <div class="list-group-card-data">
                  <p class="initiative-office">{{ card.unicefOffice }}</p>
                  <p class="initiative-name">{{ card.name }}</p>
                  <p class="initiative-date">{{ `${$gettext('Since')} ${card.lastUpdated}` }}</p>
                </div>
              </div>
            </nuxt-link>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <div class="caption">
      <div class="icon-div">
        <i class="el-icon-time"></i>
      </div>

      <p><translate>Indicates an initiative that has been in this phase for over 6 months</translate></p>
    </div>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'
import { format, differenceInDays } from 'date-fns'
export default {
  data() {
    return {
      daysStale: 180,
      phasesOmit: ['Handover or Complete', 'Discontinued'],
    }
  },
  computed: {
    ...mapGetters({
      phases: 'projects/getStages',
      landingProjectsList: 'landing/getCountryProjectsList',
      unicefOffice: 'offices/getOffices',
      sectors: 'projects/getSectors',
    }),
    omitedPhasesCount() {
      const columns = this.phases
        .filter((phase) => !this.phasesOmit.some((omphase) => omphase === phase.name))
        .sort((a, b) => a.order - b.order)
      const colsWithCount = columns.map((col) => ({
        count: this.landingProjectsList.filter((project) => project.current_phase === col.id).length,
        ...col,
      }))
      return [{ name: '', id: 'sectors', count: null }, ...colsWithCount]
    },
    includedPhasesInitiatives() {
      const phaseIdsOmit = this.phasesOmit.map((phaseName) => this.phases.find((phase) => phase.name === phaseName).id)
      return this.landingProjectsList.filter(
        (project) => !phaseIdsOmit.some((phaseId) => phaseId === project.current_phase)
      )
    },
    initiativesTableData() {
      let tableData = []

      const omPhases = this.phases.filter((phase) => !this.phasesOmit.some((omphase) => omphase === phase.name))
      const sortedSectors = this.sectors.sort((a, b) => a.name.localeCompare(b.name))
      sortedSectors.map((sector) => {
        const dataObj = {}
        dataObj['sector'] = { sector_name: sector.name }
        omPhases.map((phase) => {
          dataObj[phase.id] = []
        })
        const sectorInitiatives = this.includedPhasesInitiatives.filter((initiative) =>
          initiative.unicef_leading_sector.some((lsector) => lsector === sector.id)
        )
        sectorInitiatives.map((initiative) => {
          const lastUpdated = this.calcLastUpdated(initiative)

          let isStale = differenceInDays(new Date(), lastUpdated) > this.daysStale ? true : false

          /*Create the card and add it to tableData **/
          dataObj[`${initiative.current_phase}`] = [
            ...dataObj[`${initiative.current_phase}`],
            {
              ...initiative,
              lastUpdated: lastUpdated,
              unicefOffice: this.unicefOffice
                .find((office) => office.id === initiative.country_office)
                .name.split(':')[1],
              stale: isStale,
            },
          ]
        })

        tableData.push(this.sortCards(dataObj))
      })
      const nonEmptyRowTableData = this.removeEmptyRows(tableData)

      return this.includedPhasesInitiatives.length > 0 ? nonEmptyRowTableData : []
    },
  },
  methods: {
    calcLastUpdated(initiative) {
      if (initiative.stages && initiative.stages.length > 0) {
        /*
          Some initiatives have equal current_phase as the last phase in stages field
          Some other initiatives have equal current_phase -1 as the last phase in stages field
          Added also 
           **/
        const prevPhase = initiative.stages.find((stage) => stage.id === initiative.current_phase - 1)
        const lastPhase = initiative.stages.find((stage) => stage.id === initiative.current_phase)
        if (lastPhase) {
          return lastPhase.date
        } else if (prevPhase) {
          return prevPhase.date
        }
      } else {
        return initiative.start_date ? format(initiative.start_date, 'YYYY-MM-DD') : new Date()
      }
    },
    sortCards(dataObj) {
      for (const key in dataObj) {
        if (key !== 'sector') {
          const staleInit = dataObj[key]
            .filter((initiative) => initiative.stale === true)
            .sort((a, b) => a.name.localeCompare(b.name))
          const notStateInit = dataObj[key]
            .filter((initiative) => initiative.stale === false)
            .sort((a, b) => a.name.localeCompare(b.name))
          dataObj[key] = [...staleInit, ...notStateInit]
        }
      }
      return dataObj
    },
    removeEmptyRows(data) {
      return data.filter((row) => {
        let keep = false
        for (const key in row) {
          if (key !== 'sector') {
            if (row[key].length > 0) {
              keep = true
            }
          }
        }
        return keep
      })
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';
.LandingInitiativesTable {
  margin: 10px 0;

  .el-table--enable-row-hover .el-table__body tr:hover > td {
    background-color: unset;
  }

  .el-table {
    border: solid @colorBrandPrimary 2px;
    overflow-x: auto;

    td {
      border-left: dashed @colorBrandPrimary 1px;
    }
    td:first-child {
      border-left: none;
    }

    th {
      background-color: @colorBrandPrimary;

      padding: 0;

      > .cell {
        font-size: @fontSizeSmall;
        color: @colorWhite;
        font-weight: bold;
        height: 68px;
        #header {
          height: inherit;
          display: flex;
          justify-content: space-between;
          flex-direction: column;
          padding-top: 2px;
          #header-title {
            text-align: center;
            word-wrap: normal;
            white-space: normal;
            word-break: normal;
            text-overflow: unset;
            line-height: 20px;
            margin-top: 0;
            margin-bottom: auto;
          }
          #header-count {
            text-align: center;
            line-height: 26px;
            margin-top: auto;
            margin-bottom: 0;
          }
        }
      }

      &.is-leaf {
        border-bottom-color: @colorWhite;
      }
    }
  }
  .el-table__row {
    background-color: #f5fafc;

    > td {
      vertical-align: top;
    }
  }

  .link-card {
    text-decoration: none;
    margin: auto;

    .list-group-card {
      border: solid 1px #d0dadf;
      box-shadow: 0px 2px 1px 0px rgba(194, 204, 210, 1);
      margin: 18px 0;
      border-top-color: @colorBrandPrimary;
      border-top-width: 5px;
      border-radius: 2px;
      background-color: #ffffff;

      .list-group-card-data {
        padding: 4px 8px;
      }
      .icon-div {
        position: absolute;
        right: 24px;

        .el-icon-time {
          display: none;
        }
      }

      .initiative-name {
        padding: 0;
        margin: 0;
        display: -webkit-box;
        max-width: inherit;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
      .initiative-date {
        padding: 0;
        margin: 0;

        color: #909496;
      }

      .initiative-office {
        padding: 0;
        margin: 0;

        color: #22ace2;
      }
    }
    &.stale {
      .list-group-card {
        border-top-color: #fe8900;
        .icon-div {
          .el-icon-time {
            display: flex;

            font-size: 18px;
            background-color: #fe8900;
            border-radius: 0 0 2px 2px;
            box-shadow: 0px 1px 1px 0px rgba(194, 204, 210, 1);
            color: white;
            padding: 2px;
          }
        }
        .initiative-office {
          color: #fe8900;
        }
        .initiative-date {
          color: #fe8900;
        }
      }
    }
  }
}
.caption {
  width: 420px;
  display: inline-flex;
  padding: 10px;
  margin: 20px 0 20px 0;
  .icon-div {
    width: fit-content;
    height: fit-content;
    background-color: #fe8900;
    border-radius: 6px;
    box-shadow: 0px 4px 4px 0px rgba(194, 204, 210, 1);
    padding: 4px;
    margin-right: 10px;
    .el-icon-time {
      font-size: 36px;
      color: white;
    }
  }
  p {
    margin: 0 0 0 10px;
  }
}
</style>
