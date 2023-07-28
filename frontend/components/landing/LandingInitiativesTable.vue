<template>
  <div class="LandingInitiativesTable">
    <div class="TopSwitchBar">
      <div class="Select-sectors">
        <el-popover
          data-test="sectors-select"
          v-model="columnSelectorOpen"
          :title="settingsTitle"
          placement="bottom-end"
          width="420"
          trigger="click"
          popper-class="CustomPopover popoverAlign"
          @show="popperOpenHandler"
        >
          <el-button slot="reference" type="text" class="cogIcon">
            <fa icon="cog" />
            <translate id="select-sectors-label">Select sectors</translate>
          </el-button>

          <div class="CustomPopoverList Small ColumnSelector">
            <ul class="ColumnList">
              <li
                v-for="c in getSelectedSectors"
                :key="c.id"
                :class="['Item', { Selected: c.selected }]"
                @click="() => invertSelectSector(c.id)"
              >
                <fa icon="check" />
                {{ c.name }}
              </li>
            </ul>
            <div class="CustomPopoverActions">
              <el-row type="flex" align="middle">
                <el-col>
                  <el-button
                    data-test="select-sectors-cancel"
                    type="text"
                    size="small"
                    class="CancelButton"
                    @click="columnSelectorOpen = false"
                  >
                    <translate>Cancel</translate>
                  </el-button>
                </el-col>
                <el-col>
                  <el-button
                    data-test="select-sectors-deselect-all"
                    type="text"
                    size="small"
                    class="CancelButton"
                    @click="deselectAllSectors"
                  >
                    <translate>Deselect all</translate>
                  </el-button>
                </el-col>
                <el-col>
                  <el-button
                    data-test="select-sectors-select-all"
                    type="text"
                    size="small"
                    class="CancelButton"
                    @click="selectAllSectors"
                  >
                    <translate>Select all</translate>
                  </el-button>
                </el-col>
                <el-col>
                  <el-button
                    data-test="select-sectors-update"
                    type="text"
                    size="small"
                    class="PrimaryButton"
                    @click="updateSectors"
                  >
                    <translate>Update</translate>
                  </el-button>
                </el-col>
              </el-row>
            </div>
          </div>
        </el-popover>
      </div>
      <div>
        <el-switch
          data-test="height-switch"
          v-model="stdHeight"
          :active-text="$gettext('Standard height') | translate"
          :inactive-text="$gettext('Full height') | translate"
          class="Switch"
        >
        </el-switch>
        <el-switch
          data-test="phases-stages-switch"
          v-model="boardType"
          :active-text="$gettext('Phases board') | translate"
          :inactive-text="$gettext('Stages board') | translate"
          class="Switch"
        >
        </el-switch>
      </div>
    </div>
    <el-table
      :data="initiativesTableData"
      :highlight-current-row="false"
      :key="stdHeight ? 'custom' : 'full'"
      v-bind="setMaxHeight"
      :lazy="true"
      stripe
      :empty-text="$gettext('No initiatives') | translate"
    >
      <template slot="empty">
        <translate key="empty-sector-initiatives-table-text">No initiatives to show</translate>
      </template>
      <el-table-column
        v-for="({ name, id, count }, index) in columns"
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
          <div v-if="index === 0" class="sectors-cell">
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
                  <p class="initiative-office">{{ card.title }}</p>
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
      boardType: true,
      stdHeight: true,
      columnSelectorOpen: false,
    }
  },
  mounted() {
    this.$store.dispatch('phasesStagesBoard/initSectors')
  },
  computed: {
    ...mapGetters({
      phases: 'projects/getStages',
      landingProjectsList: 'landing/getCountryProjectsList',
      unicefOffice: 'offices/getOffices',
      phasesStages: 'projects/getPhasesStages',
      unicef_regions: 'system/getUnicefRegions',
      getSelectedSectors: 'phasesStagesBoard/getSelectedSectors',
      getShownSectors: 'phasesStagesBoard/getShownSectors',
    }),
    settingsTitle() {
      return `${this.$gettext('selected sectors')} (${
        this.getSelectedSectors.filter((sector) => sector.selected === true).length
      }/${this.getSelectedSectors.length})`
    },
    setMaxHeight() {
      return this.stdHeight ? { 'max-height': 580 } : { 'max-height': false }
    },
    columns() {
      return this.boardType ? this.omitedPhasesCount : this.stagesCount
    },
    stagesCount() {
      const columns = this.phasesStages.map((phst) => ({ name: phst.stage_label, id: phst.stage_number }))
      const colsWithCount = columns.map((col) => ({
        count: this.landingProjectsList.filter((project) => this.getStage(project.current_phase) === col.id).length,
        ...col,
      }))
      return [{ name: '', id: 'sectors', count: null }, ...colsWithCount]
    },
    omitedPhasesCount() {
      const columns = this.phases.filter((phase) => !phase.end_phase).sort((a, b) => a.order - b.order)
      const colsWithCount = columns.map((col) => ({
        count: this.landingProjectsList.filter((project) => project.current_phase === col.id).length,
        ...col,
      }))
      return [{ name: '', id: 'sectors', count: null }, ...colsWithCount]
    },
    includedPhasesInitiatives() {
      const phaseIdsOmit = this.phases.filter((phase) => phase.end_phase).map((phase) => phase.id)
      return this.landingProjectsList.filter(
        (project) => !phaseIdsOmit.some((phaseId) => phaseId === project.current_phase)
      )
    },
    sortedSelectedSectors() {
      return this.getShownSectors
        .sort((a, b) => a.name.localeCompare(b.name))
        .filter((sector) => sector.selected === true)
    },
    initiativesTableData() {
      return this.boardType ? this.initiativesPhasesTableData : this.initiativesStagesTableData
    },
    initiativesStagesTableData() {
      let tableData = []
      /* Creates each table row per sector**/
      this.sortedSelectedSectors.map((sector) => {
        const dataObj = {}
        dataObj['sector'] = { sector_name: sector.name }
        this.phasesStages.map((stage) => {
          dataObj[stage.stage_number] = []
        })
        /* Filters the relative initiatives **/
        const sectorInitiatives = this.landingProjectsList.filter((project) =>
          project.unicef_leading_sector.some((lsector) => lsector === sector.id)
        )
        sectorInitiatives.map((initiative) => {
          const lastUpdated = this.calcLastUpdated(initiative)

          let isStale = differenceInDays(new Date(), lastUpdated) > this.daysStale ? true : false

          /*Create the card and add it to tableData **/
          const regionId = this.unicefOffice.find((office) => office.id === initiative.country_office).region
          const regionName = this.unicef_regions.find((region) => region.id === regionId).name
          dataObj[`${this.getStage(initiative.current_phase)}`] = [
            ...dataObj[`${this.getStage(initiative.current_phase)}`],
            {
              ...initiative,
              lastUpdated: lastUpdated,
              title: regionName,
              stale: isStale,
            },
          ]
        })

        tableData.push(this.sortCards(dataObj))
      })

      return this.removeEmptyRows(tableData)
    },
    initiativesPhasesTableData() {
      let tableData = []

      const omPhases = this.phases.filter((phase) => !phase.end_phase)
      /* Creates each table row per sector**/
      this.sortedSelectedSectors.map((sector) => {
        const dataObj = {}
        dataObj['sector'] = { sector_name: sector.name }
        omPhases.map((phase) => {
          dataObj[phase.id] = []
        })
        /* Filters the relative initiatives **/
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
              title: this.unicefOffice.find((office) => office.id === initiative.country_office).name.split(':')[1],
              stale: isStale,
            },
          ]
        })

        tableData.push(this.sortCards(dataObj))
      })

      return this.removeEmptyRows(tableData)
    },
  },
  methods: {
    deselectAllSectors() {
      this.$store.dispatch('phasesStagesBoard/deselectAll')
    },
    selectAllSectors() {
      this.$store.dispatch('phasesStagesBoard/selectAll')
    },
    updateSectors() {
      this.$store.dispatch('phasesStagesBoard/updateSectors')
      this.columnSelectorOpen = false
    },
    invertSelectSector(sectorId) {
      this.$store.dispatch('phasesStagesBoard/invertSelectSector', sectorId)
    },
    getStage(phase) {
      return this.phasesStages.find((stage) => stage.phases.some((stphase) => stphase.phase_number === phase))
        .stage_number
    },
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
  padding-top: 30px;
  margin: 20px 0 60px 0;

  .TopSwitchBar {
    width: 100%;
    height: 30px;
    display: flex;
    justify-content: space-between;

    .Select-sectors {
      padding-left: @leftHomepageIndentation;

      span {
        position: relative;
        top: 1px;
        #select-sectors-label {
          position: relative;
          font-size: 14px;
          font-weight: normal;
          top: -2px;
        }
        .cogIcon {
          padding: unset;
          .fa-cog {
            padding: 4px 8px 0 0;
            font-size: 18px;
          }
        }
      }
    }

    .Switch {
      padding: 5px 18px 0;
    }
  }

  .el-table {
    overflow-x: auto;

    .sectors-cell {
      text-align: end;
      font-weight: bold;
    }

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
            font-size: @fontSizeSmall;
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
  .el-table__row .hover-row {
    > tr {
      > td {
        background-color: unset !important;
      }
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
.popoverAlign {
  transform: translate(-5px, 0px);
  margin: 0 28px;
}

.caption {
  width: 340px;
  display: inline-flex;
  padding: 10px 10px 10px @leftHomepageIndentation;
  margin: 20px 0 20px 0;
  .icon-div {
    width: fit-content;
    height: 20px;
    background-color: #fe8900;
    border-radius: 6px;
    box-shadow: 0px 4px 4px 0px rgba(194, 204, 210, 1);
    padding: 4px;
    margin-right: 10px;
    .el-icon-time {
      font-size: 20px;
      color: white;
    }
  }
  p {
    margin: 0 0 0 10px;
    font-size: @fontSizeSmall;
  }
}
.el-table--striped .el-table__body tr.el-table__row--striped td {
  background-color: unset !important;
}
.el-table__body tr.hover-row > td,
.el-table__body tr.hover-row.current-row > td,
.el-table__body tr.hover-row.el-table__row--striped > td,
.el-table__body tr.hover-row.el-table__row--striped.current-row > td {
  background-color: unset !important;
}
</style>
