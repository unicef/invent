<template>
  <div class="LandingInitiativesTable">
    <el-table
      :data="initiativesTableData"
      :highlight-current-row="false"
      max-height="600"
      :lazy="true"
      :empty-text="$gettext('No initiatives available') | translate"
    >
      <el-table-column
        v-for="{ name, id } in ommitedPhases"
        :label="$gettext(name) | translate"
        :prop="name"
        :key="id"
        min-width="180"
      >
        <template slot-scope="scope">
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
    }),
    ommitedPhases() {
      return this.phases
        .filter((phase) => !this.phasesOmit.some((omphase) => omphase === phase.name))
        .sort((a, b) => a.order - b.order)
    },
    initiativesTableData() {
      const dataObj = {}
      this.phases.map((phase) => {
        dataObj[phase.id] = []
      })
      const initiatives = this.landingProjectsList

      initiatives.map((initiative) => {
        let lastUpdated
        if (initiative.stages && initiative.stages.length > 0) {
          /*
          Some initiatives have equal current_phase as the last phase in stages field
          Some other initiatives have equal current_phase -1 as the last phase in stages field
          Added also 
           **/
          const prevPhase = initiative.stages.find((stage) => stage.id === initiative.current_phase - 1)
          const lastPhase = initiative.stages.find((stage) => stage.id === initiative.current_phase)
          if (lastPhase) {
            lastUpdated = lastPhase.date
          } else if (prevPhase) {
            lastUpdated = prevPhase.date
          }
        } else {
          lastUpdated = initiative.start_date ? format(initiative.start_date, 'YYYY-MM-DD') : new Date()
        }

        let isStale = differenceInDays(new Date(), lastUpdated) > this.daysStale ? true : false

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

      for (const key in dataObj) {
        const staleInit = dataObj[key]
          .filter((initiative) => initiative.stale === true)
          .sort((a, b) => a.name.localeCompare(b.name))
        const notStateInit = dataObj[key]
          .filter((initiative) => initiative.stale === false)
          .sort((a, b) => a.name.localeCompare(b.name))
        dataObj[key] = [...staleInit, ...notStateInit]
      }

      return initiatives.length > 0 ? [dataObj] : null
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
      vertical-align: top;
      > .cell {
        word-wrap: normal;
        white-space: normal;
        word-break: normal;
        text-overflow: unset;

        font-size: @fontSizeSmall;
        color: @colorWhite;
        font-weight: bold;
        letter-spacing: 0;
        line-height: 29px;
        text-align: start;
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
        z-index: 10;

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
