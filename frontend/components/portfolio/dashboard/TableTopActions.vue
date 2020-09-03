<template>
  <div class="actions">
    <div class="left">
      <el-button size="small" type="text" @click="toggleSelectAll">
        <translate v-show="!allSelected" :parameters="{ total }">
          Select all {total} projects
        </translate>
        <translate v-show="allSelected" :parameters="{ total }">
          Deselect all {total} projects
        </translate>
      </el-button>
      <list-export :projects="rowToExport">
        <template #default="{parsed}">
          <xlsx-workbook>
            <xlsx-sheet :collection="parsed" sheet-name="export" />
            <xlsx-download
              disable-wrapper-click
              :options="{ bookType: exportType.toLowerCase() }"
              :filename="`export.${exportType.toLowerCase()}`"
            >
              <template #default="{download}">
                <el-button
                  :disabled="selectedRows.length === 0"
                  type="text"
                  size="small"
                  class="IconLeft"
                  @click="exportRows(download)"
                >
                  <span>
                    <translate>Export selected</translate>
                  </span>
                </el-button>
              </template>
            </xlsx-download>
          </xlsx-workbook>
        </template>
      </list-export>
      <el-select
        v-model="exportType"
        :disabled="selectedRows.length === 0"
        size="small"
      >
        <el-option label="CSV" value="CSV" />
        <el-option label="XLSX" value="XLSX" />
        <el-option label="PDF" value="PDF" />
      </el-select>
    </div>
    <div class="right">Actions</div>
  </div>
</template>

<script>
import { XlsxWorkbook, XlsxSheet, XlsxDownload } from "vue-xlsx";
import PdfExport from "@/components/dashboard/PdfExport";
import ListExport from "@/components/dashboard/ListExport";

import { mapGetters, mapActions } from "vuex";

export default {
  components: {
    PdfExport,
    XlsxWorkbook,
    XlsxSheet,
    XlsxDownload,
    ListExport
  },
  data() {
    return {
      exportType: "XLSX",
      columnSelectorOpen: false,
      selectedColumns: [],
      viewportSize: 2000
    };
  },
  computed: {
    ...mapGetters({
      columns: "dashboard/getAvailableColumns",
      selectedCol: "dashboard/getSelectedColumns",
      selectedRows: "dashboard/getSelectedRows",
      allSelected: "dashboard/getSelectAll",
      total: "dashboard/getTotal",
      user: "user/getProfile",
      projects: "dashboard/getProjectsBucket",
      dashboardId: "dashboard/getDashboardId",
      dashboardType: "dashboard/getDashboardType"
    }),
    settingsTitle() {
      return `${this.$gettext("main fields")} (${this.selectedCol.length}/${
        this.columns.length
      })`;
    },
    selected() {
      return this.allSelected ? this.total : this.selectedRows.length;
    },
    rowToExport() {
      return this.allSelected
        ? this.projects
        : this.projects.filter(p => this.selectedRows.some(sr => sr === p.id));
    },
    showEmailButton() {
      const allowed = ["CA", "SCA", "D", "DA", "SDA"];
      if (this.user) {
        return (
          allowed.includes(this.user.account_type) || this.user.is_superuser
        );
      }
      return false;
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.setViewport();
      window.addEventListener("resize", this.setViewport);
    });
  },
  beforeDestroy() {
    if (process.client) {
      window.removeEventListener("resize", this.setViewport);
    }
  },
  methods: {
    ...mapActions({
      setSelectedColumns: "dashboard/setSelectedColumns",
      setSelectAll: "dashboard/setSelectAll",
      setSendEmailDialogState: "layout/setSendEmailDialogState",
      loadProjectsBucket: "dashboard/loadProjectsBucket",
      setSelectedRows: "dashboard/setSelectedRows"
    }),
    setViewport() {
      if (process.client && window) {
        this.viewportSize = window.innerWidth;
      }
    },
    popperOpenHandler() {
      this.selectedColumns = [...this.columns.map(s => ({ ...s }))];
    },
    updateColumns() {
      this.setSelectedColumns(
        this.selectedColumns.filter(s => s.selected).map(s => s.id)
      );
      this.columnSelectorOpen = false;
    },
    async toggleSelectAll() {
      if (!this.allSelected) {
        await this.loadProjectsBucket();
        this.setSelectAll(true);
      } else {
        this.setSelectAll(false);
        this.setSelectedRows([]);
      }
    },
    exportRows(xlsxDownloadFunction) {
      this.$nuxt.$loading.start("pdf");
      window.setTimeout(async () => {
        if (this.exportType === "PDF") {
          this.$refs.pdfExport.printPdf();
        } else {
          xlsxDownloadFunction();
        }
        this.$nuxt.$loading.finish("pdf");
      }, 500);
    },
    async openMailDialog() {
      if (this.allSelected) {
        await this.loadProjectsBucket();
      }
      this.setSendEmailDialogState(true);
    }
  }
};
</script>

<style lang="less" scoped>
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

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
}
</style>
