<template>
  <div class="actions">
    <div class="left">
      <el-button size="small" type="text" @click="toggleSelectAll">
        <translate v-show="!allSelected" :parameters="{ total }">
          Select all {total} initiatives
        </translate>
        <translate v-show="allSelected" :parameters="{ total }">
          Deselect all {total} initiatives
        </translate>
      </el-button>
      <ListExport :projects="rowToExport">
        <template #default="{ parsedScores }">
          <xlsx-workbook>
            <xlsx-sheet :collection="parsedScores" sheet-name="export" />
            <xlsx-download
              disable-wrapper-click
              :options="{ bookType: exportType.toLowerCase() }"
              :filename="`export.${exportType.toLowerCase()}`"
            >
              <template #default="{ download }">
                <el-button
                  :disabled="selectedRows.length === 0"
                  type="text"
                  size="small"
                  class="IconLeft"
                  @click="exportRows(download)"
                >
                  <fa icon="download" />
                  <span v-show="selectedRows.length === 0">
                    <translate>Export selected</translate>
                  </span>
                  <span v-show="selected">
                    <translate :parameters="{ selected }">
                      Export {selected} selected
                    </translate>
                  </span>
                </el-button>
              </template>
            </xlsx-download>
          </xlsx-workbook>
        </template>
      </ListExport>
      <el-select v-model="exportType" :disabled="disabled" size="small">
        <el-option label="CSV" value="CSV" />
        <el-option label="XLSX" value="XLSX" />
        <!-- <el-option label="PDF" value="PDF" /> -->
      </el-select>
    </div>
    <div class="right">
      <div class="settings">
        <el-popover
          v-model="columnSelectorOpen"
          :title="settingsTitle"
          placement="bottom-end"
          width="264"
          trigger="click"
          popper-class="CustomPopover TableSettingsDropdown"
          @show="popperOpenHandler"
        >
          <el-button
            slot="reference"
            type="text"
            class="TableSettingsButton IconLeft"
          >
            <fa icon="cog" />
          </el-button>
          <div class="CustomPopoverList Small ColumnSelector">
            <ul class="ColumnList">
              <li
                v-for="c in selectedColumns"
                :key="c.id"
                :class="['Item', { Selected: c.selected }]"
                @click="c.selected = !c.selected"
              >
                <fa icon="check"></fa>
                <info-popover
                  v-if="c.id === '61' || c.id == '62'"
                  placement="right"
                  width="360"
                  class="hint-icon"
                  :icon="['fas', 'info-circle']"
                  ><translate v-if="c.id === '61'" key="noexport"
                    >This field represents the reviewers' scores and inputs
                    assigned to the project. They will be exported horizontally
                    in the projects' row.</translate
                  ><translate v-else
                    >Official scores will be exported horizontally in the
                    projects' row.</translate
                  >
                </info-popover>
                {{ c.label }}
              </li>
            </ul>
            <div class="CustomPopoverActions">
              <el-row type="flex" align="middle">
                <el-col>
                  <el-button
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
                    type="text"
                    size="small"
                    class="CancelButton"
                    @click="deselectAllCols"
                  >
                    <translate>Deselect all</translate>
                  </el-button>
                </el-col>
                <el-col>
                  <el-button
                    type="text"
                    size="small"
                    class="PrimaryButton"
                    @click="updateColumns"
                  >
                    <translate>Update</translate>
                  </el-button>
                </el-col>
              </el-row>
            </div>
          </div>
        </el-popover>
      </div>
      <div class="move">
        <small>
          <translate>Actions:</translate>
        </small>
        <el-tooltip v-if="tab !== 1" :content="moveTo[back]" placement="top">
          <el-button
            type="danger"
            size="small"
            circle
            :disabled="disabled"
            @click="handleClickBack"
          >
            <fa icon="arrow-left" />
          </el-button>
        </el-tooltip>
        <el-tooltip v-if="tab !== 3" :content="moveTo[forward]" placement="top">
          <el-button
            type="success"
            size="small"
            circle
            :disabled="disabled"
            @click="handleClickForward"
          >
            <fa icon="arrow-right" />
          </el-button>
        </el-tooltip>
      </div>
    </div>
  </div>
</template>

<script>
import filter from 'lodash/filter'
import flatten from 'lodash/flatten'
import pick from 'lodash/pick'
import { XlsxWorkbook, XlsxSheet, XlsxDownload } from 'vue-xlsx'
// import PdfExport from '@/components/dashboard/PdfExport'
import ListExport from '@/components/dashboard/ListExport'
import InfoPopover from '@/components/common/InfoPopover'

import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  components: {
    // PdfExport,
    XlsxWorkbook,
    XlsxSheet,
    XlsxDownload,
    ListExport,
    InfoPopover,
  },
  data() {
    return {
      exportType: 'XLSX',
      viewportSize: 2000,
      moveTo: [
        this.$gettext('Move to Inventory'),
        this.$gettext('Move to Review'),
        this.$gettext('Move to Porfolio'),
      ],
      // settings
      columnSelectorOpen: false,
      selectedColumns: [],
    }
  },
  computed: {
    ...mapState({
      tab: (state) => state.portfolio.tab,
      back: (state) => state.portfolio.back,
      forward: (state) => state.portfolio.forward,
      total: (state) => state.portfolio.total,
      portfolioPage: (state) => state.search.filter.portfolio_page,
      mapColKeys: (state) => state.dashboard.mapColKeys,
      projects: (state) => state.portfolio.projects,
    }),
    ...mapGetters({
      selectedRows: 'portfolio/getSelectedRows',
      allSelected: 'portfolio/getSelectAll',
      columns: 'dashboard/getAvailableColumns',
      selectedCol: 'dashboard/getSelectedColumns',
    }),
    selected() {
      return this.allSelected ? this.total : this.selectedRows.length
    },
    disabled() {
      return this.selectedRows.length === 0
    },
    rowToExport() {
      let projects = this.allSelected
        ? this.projects
        : this.projects.filter((p) =>
            this.selectedRows.some((sr) => sr === p.id)
          )
      let selectedCols = []
      this.mapColKeys.forEach((i) => {
        if (this.selectedCol.includes(i.id)) selectedCols.push(i.key)
      })
      selectedCols = flatten(selectedCols)
      projects = projects.map((i) => {
        return pick(i, selectedCols)
      })
      return projects
    },
    // settings
    settingsTitle() {
      return `${this.$gettext('main fields')} (${this.selectedCol.length}/${
        this.columns.length
      })`
    },
  },
  methods: {
    ...mapActions({
      setSelectAll: 'portfolio/setSelectAll',
      setSelectedRows: 'portfolio/setSelectedRows',
      moveToState: 'portfolio/moveToState',
      // settings
      setSelectedColumns: 'dashboard/setSelectedColumns',
    }),
    deselectAllCols() {
      this.selectedColumns.map((c) => (c.selected = false))
    },
    toggleSelectAll() {
      if (!this.allSelected) {
        this.setSelectAll(true)
      } else {
        this.setSelectAll(false)
        this.setSelectedRows([])
      }
    },
    exportRows(xlsxDownloadFunction) {
      this.$nuxt.$loading.start('pdf')
      window.setTimeout(() => {
        if (this.exportType === 'PDF') {
          this.$refs.pdfExport.printPdf()
        } else {
          xlsxDownloadFunction()
        }
        this.$nuxt.$loading.finish('pdf')
      }, 500)
    },
    // back and forward values
    async handleClickBack() {
      const tab = this.tab - 1
      switch (tab) {
        case 1:
          await this.moveToState({
            type: 'remove-project',
            project: this.selectedRows,
            tab,
          })
          break
        case 2:
          await this.moveToState({
            type: 'disapprove-project',
            project: this.selectedRows,
            tab,
          })
          break
        default:
          break
      }
    },
    async handleClickForward() {
      const tab = this.tab + 1
      switch (tab) {
        case 2:
          await this.moveToState({
            type: 'add-project',
            project: this.selectedRows,
            tab,
          })
          break
        case 3:
          await this.moveToState({
            type: 'approve-project',
            project: this.selectedRows,
            tab,
          })
          break
        default:
          break
      }
    },
    // settings
    popperOpenHandler() {
      const colFilter = (hide = ['61', '62']) =>
        filter(columns, (c) => !hide.includes(c.id))
      const columns = [...this.columns.map((s) => ({ ...s }))]
      if (this.$route.name.includes('organisation-portfolio-management-id')) {
        switch (this.portfolioPage) {
          case 'review':
            this.selectedColumns = columns
            break
          case 'portfolio':
            // this.selectedColumns = colFilter(['61'])
            this.selectedColumns = columns
            break
          default:
            this.selectedColumns = colFilter()
            break
        }
      } else {
        this.selectedColumns = colFilter()
      }
    },
    updateColumns() {
      this.setSelectedColumns(
        this.selectedColumns.filter((s) => s.selected).map((s) => s.id)
      )
      this.columnSelectorOpen = false
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.hint-icon {
  position: absolute;
  right: 32px;
  top: 1px;
}

::v-deep .hint-icon .question-icon {
  font-size: 14px;
}

.actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 40px 40px 30px 40px;
  .left {
    display: flex;
    align-items: center;
    & > button {
      margin-right: 40px;
    }
    & > div {
      margin-right: 20px;
    }
    .el-select {
      width: 84px;
    }
  }
  .right {
    display: flex;
    align-items: center;
    .settings {
      margin-right: 20px;
      button {
        font-size: 20px;
      }
    }
    .move {
      padding-left: 20px;
      border-left: 1px solid #eae6e2;
      small {
        font-size: 12px;
        letter-spacing: 0;
        line-height: 15px;
        margin-right: 16px;
      }
    }
  }
}

.ColumnList {
  max-height: 260px;
  overflow-y: scroll;
}
</style>
