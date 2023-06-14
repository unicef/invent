<template>
  <el-row type="flex" justify="space-between" align="middle" class="TableTopActions">
    <el-col class="TableExportOptions">
      <el-row type="flex">
        <el-button size="small" type="text" @click="toggleSelectAll">
          <translate v-show="!allSelected" :parameters="{ total }"> Select all {total} initiatives </translate>
          <translate v-show="allSelected" :parameters="{ total }"> Deselect all {total} initiatives </translate>
        </el-button>

        <div class="Separator" />
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
                      <translate :parameters="{ selected }"> Export {selected} selected </translate>
                    </span>
                  </el-button>
                </template>
              </xlsx-download>
            </xlsx-workbook>
          </template>
        </ListExport>
        <el-select v-model="exportType" size="small">
          <el-option label="CSV" value="CSV" />
          <el-option label="XLSX" value="XLSX" />
          <!-- <el-option label="PDF" value="PDF" /> -->
        </el-select>

        <template v-if="showEmailButton">
          <div class="Separator" />
          <el-button
            :disabled="selectedRows.length === 0"
            type="text"
            size="small"
            class="IconLeft"
            @click="openMailDialog"
          >
            <fa icon="envelope" />
            <translate v-show="selected === 0"> Contact selected </translate>
            <translate v-show="selected > 0" :parameters="{ selected }"> Contact {selected} selected </translate>
          </el-button>
          <pdf-export ref="pdfExport" />
        </template>
      </el-row>
    </el-col>

    <el-col class="TableLegend">
      <el-row type="flex" align="middle">
        <project-legend :compact-mode="viewportSize < 1440" force-star force-eye force-globe show-label />

        <div class="Separator" />

        <el-popover
          v-model="columnSelectorOpen"
          :title="settingsTitle"
          placement="bottom-end"
          width="420"
          trigger="click"
          popper-class="CustomPopover TableSettingsDropdown"
          @show="popperOpenHandler"
        >
          <el-button slot="reference" type="text" size="small" class="TableSettingsButton IconLeft">
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
                <fa icon="check" />
                {{ c.label }}
              </li>
            </ul>
            <div class="CustomPopoverActions">
              <el-row type="flex" align="middle">
                <el-col>
                  <el-button type="text" size="small" class="CancelButton" @click="columnSelectorOpen = false">
                    <translate>Cancel</translate>
                  </el-button>
                </el-col>
                <el-col>
                  <el-button type="text" size="small" class="CancelButton" @click="deselectAllCols">
                    <translate>Deselect all</translate>
                  </el-button>
                </el-col>
                <el-col>
                  <el-button type="text" size="small" class="PrimaryButton" @click="updateColumns">
                    <translate>Update</translate>
                  </el-button>
                </el-col>
              </el-row>
            </div>
          </div>
        </el-popover>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
import filter from 'lodash/filter'
import flatten from 'lodash/flatten'
import pick from 'lodash/pick'
import { XlsxWorkbook, XlsxSheet, XlsxDownload } from 'vue-xlsx'
import ListExport from '@/components/dashboard/ListExport'
import { mapState, mapGetters, mapActions } from 'vuex'
import ProjectLegend from '../common/ProjectLegend'
import PdfExport from './PdfExport'

export default {
  components: {
    ProjectLegend,
    PdfExport,
    XlsxWorkbook,
    XlsxSheet,
    XlsxDownload,
    ListExport,
  },
  data() {
    return {
      exportType: 'XLSX',
      columnSelectorOpen: false,
      selectedColumns: [],
      viewportSize: 2000,
    }
  },
  computed: {
    ...mapState({
      mapColKeys: (state) => state.dashboard.mapColKeys,
    }),
    ...mapGetters({
      columns: 'dashboard/getAvailableColumns',
      selectedCol: 'dashboard/getSelectedColumns',
      selectedRows: 'dashboard/getSelectedRows',
      allSelected: 'dashboard/getSelectAll',
      total: 'dashboard/getTotal',
      user: 'user/getProfile',
      projects: 'dashboard/getProjectsBucket',
    }),
    settingsTitle() {
      return `${this.$gettext('main fields')} (${this.selectedCol.length}/${this.columns.length})`
    },
    selected() {
      return this.allSelected ? this.total : this.selectedRows.length
    },
    rowToExport() {
      let projects = this.allSelected
        ? this.projects
        : this.projects.filter((p) => this.selectedRows.some((sr) => sr === p.id))
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
    showEmailButton() {
      const allowed = ['CA', 'SCA', 'D', 'DA', 'SDA']
      if (this.user) {
        return allowed.includes(this.user.account_type) || this.user.is_superuser
      }
      return false
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.setViewport()
      window.addEventListener('resize', this.setViewport)
    })
  },
  beforeDestroy() {
    // eslint-disable-next-line
    if (process.client) {
      window.removeEventListener('resize', this.setViewport)
    }
  },
  methods: {
    ...mapActions({
      setSelectedColumns: 'dashboard/setSelectedColumns',
      setSelectAll: 'dashboard/setSelectAll',
      setSendEmailDialogState: 'layout/setSendEmailDialogState',
      loadProjectsBucket: 'dashboard/loadProjectsBucket',
      setSelectedRows: 'dashboard/setSelectedRows',
    }),
    setViewport() {
      if (process.client && window) {
        this.viewportSize = window.innerWidth
      }
    },
    popperOpenHandler() {
      const colFilter = (hide = ['61', '62']) => filter(columns, (c) => !hide.includes(c.id))
      const columns = [...this.columns.map((s) => ({ ...s }))]
      this.selectedColumns = colFilter()
    },
    updateColumns() {
      this.setSelectedColumns(this.selectedColumns.filter((s) => s.selected).map((s) => s.id))
      this.columnSelectorOpen = false
    },
    deselectAllCols() {
      this.selectedColumns.map((c) => (c.selected = false))
    },
    async toggleSelectAll() {
      if (!this.allSelected) {
        await this.loadProjectsBucket()
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
    async openMailDialog() {
      if (this.allSelected) {
        await this.loadProjectsBucket()
      }
      this.setSendEmailDialogState(true)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.TableTopActions {
  width: calc(100vw - @advancedSearchWidth);
  min-width: @appWidthMinLimit - @advancedSearchWidth;
  max-width: @appWidthMaxLimit - @advancedSearchWidth;
  // height: @tableTopActionsHeight;
  padding: 40px 40px 30px 40px;

  .Separator {
    .SeparatorStyle();
    height: 32px;
    margin: 0 20px;
  }

  .TableExportOptions {
    width: 100%;

    .el-button {
      &.is-disabled {
        + .el-select {
          display: none;
        }
      }
    }

    .el-select {
      width: 84px;
      margin-left: 10px;
    }
  }

  .TableLegend {
    width: auto;
    height: 32px;

    .ProjectLegend {
      font-size: @fontSizeSmall;
      // color: @colorTextSecondary;
      white-space: nowrap;
      padding-top: 0px;

      .svg-inline--fa {
        position: relative;
        vertical-align: middle;
        height: 14px;
        margin-left: 20px;
        margin-right: 6px;
        // color: @colorTextSecondary;
        font-size: 10px;

        &.fa-star {
          top: -1px;
          font-size: 11px;
        }
      }
    }

    .ShowLegendButton {
      color: @colorTextSecondary;

      .svg-inline--fa {
        height: 12px;
        margin-left: 0;
        color: @colorTextSecondary;
      }
    }

    .TableSettingsButton {
    }
  }
}

.TableSettingsDropdown {
  transform: translate(10px, -30px);
}

.TableLegendDropdown {
  transform: translate(10px, -30px);

  .ProjectLegendContent {
    padding: 8px 12px 12px;

    > span {
      position: relative;
      display: block;

      .svg-inline--fa {
        position: absolute;
        top: 3px;
        left: 0;
        height: 14px;
        margin-right: 6px;

        &.fa-handshake {
          left: -1px;
        }
      }

      > span {
        margin-left: 20px;
        font-size: @fontSizeSmall;
      }
    }
  }
}

.ColumnList {
  max-height: 260px;
  overflow-y: scroll;
}
</style>
