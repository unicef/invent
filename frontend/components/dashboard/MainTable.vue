<template>
  <div class="MainTable">
    <el-table
      ref="mainTable"
      :data="projectsList"
      :max-height="tableMaxHeight"
      :row-class-name="rowClassCalculator"
      :stripe="false"
      :border="true"
      size="mini"
      style="width: 100%"
      @select="selectHandler"
      @select-all="selectHandler"
      @sort-change="sortChanged"
    >
      <el-table-column
        :resizable="false"
        type="selection"
        align="center"
        width="35"
      />
      <el-table-column
        v-if="selectedColumns.includes('1')"
        :resizable="false"
        :label="$gettext('Project Name') | translate"
        fixed
        sortable="custom"
        prop="project__name"
        width="240"
      >
        <template slot-scope="scope">
          <project-card
            :project="scope.row"
            hide-borders
            show-verified
          />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('5')"
        :resizable="false"
        :label="$gettext('Region') | translate"
        sortable="custom"
        prop="country__region"
        width="180"
      >
        <template slot-scope="scope">
          <region-item
            :id="scope.row.region"
          />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('2')"
        :resizable="false"
        :label="$gettext('Country') | translate"
        sortable="custom"
        prop="country__name"
        width="180"
      >
        <template slot-scope="scope">
          <country-item
            :id="scope.row.country"
            :show-flag="false"
          />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('3')"
        :resizable="false"
        :label="$gettext('Last updated') | translate"
        sortable="custom"
        prop="project__modified"
        width="180"
      >
        <template slot-scope="scope">
          {{ convertDate(scope.row.modified) }}
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('16')"
        :resizable="false"
        :label="$gettext('Field office') | translate"
        width="180"
      >
        <template slot-scope="scope">
          <FieldOfficeItem
            :value="scope.row.field_office"
            :country="scope.row.country"
          />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('11')"
        :resizable="false"
        :label="$gettext('Goal Area') | translate"
        width="180"
      >
        <template slot-scope="scope">
          <GoalAreaItem
            :value="scope.row.goal_area"
          />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('12')"
        :resizable="false"
        :label="$gettext('Result Area') | translate"
        width="180"
      >
        <template slot-scope="scope">
          <ResultAreaItem
            :value="scope.row.result_area"
          />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('13')"
        :resizable="false"
        :label="$gettext('Capability Levels') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <CapabilitiesList
            show-icon
            :value="scope.row.capability_levels"
            :goal-area="scope.row.goal_area"
            :values-function="getCapabilityLevels"
          />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('14')"
        :resizable="false"
        :label="$gettext('Capability Categories') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <CapabilitiesList
            show-icon
            :value="scope.row.capability_categories"
            :goal-area="scope.row.goal_area"
            :values-function="getCapabilityCategories"
          />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('15')"
        :resizable="false"
        :label="$gettext('Capability Subcategories') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <CapabilitiesList
            show-icon
            :value="scope.row.capability_subcategories"
            :goal-area="scope.row.goal_area"
            :values-function="getCapabilitySubcategories"
          />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('6')"
        :resizable="false"
        :label="$gettext('Investors') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <donors-list
            :value="scope.row.donors"
            :limit="3"
            show-icon
          />
        </template>
      </el-table-column>
      <el-table-column
        v-if="selectedColumns.includes('7')"
        :resizable="false"
        :label="$gettext('Programme Focal Point Name') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.contact_name }}</span>
          <a
            :href="`mailto:${scope.row.contact_email}`"
            :rel="`email`"
            class="TextLink"
          >
            {{ scope.row.contact_email }}
          </a>
        </template>
      </el-table-column>
      <el-table-column
        v-if="selectedColumns.includes('8')"
        :resizable="false"
        :label="$gettext('Initiative Description') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.implementation_overview }}</p>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('10')"
        :resizable="false"
        :label="$gettext('Health Focus Areas') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <HfaCategoriesList
            :value="scope.row.health_focus_areas"
            :limit="3"
            value-is-child
            show-check
          />
        </template>
      </el-table-column>

      <el-table-column
        v-for="col in countryColumns"
        :key="col.id"
        :resizable="false"
        :render-header="customHeaderRenderer"
        :label="col.label"
        width="240"
      >
        <template slot-scope="scope">
          <custom-answers-cell
            :id="col.originalId"
            :row="scope.row"
            :type="col.type"
            :limit="3"
          />
        </template>
      </el-table-column>

      <el-table-column
        v-for="col in donorColumns"
        :key="col.id"
        :resizable="false"
        :render-header="customHeaderRenderer"
        :label="col.label"
        width="240"
      >
        <template slot-scope="scope">
          <custom-answers-cell
            :id="col.originalId"
            :row="scope.row"
            :type="col.type"
            :donor-id="col.donorId"
            :limit="3"
          />
        </template>
      </el-table-column>
    </el-table>

    <div class="Pagination">
      <el-pagination
        :current-page.sync="currentPage"
        :page-size.sync="pageSize"
        :page-sizes="pageSizeOption"
        :total="total"
        :layout="paginationOrderStr"
      >
        <current-page />
      </el-pagination>
    </div>
  </div>
</template>

<script>
import { format } from 'date-fns';
import { mapGetters, mapActions } from 'vuex';
import { mapGettersActions } from '../../utilities/form.js';

import ProjectCard from '@/components/common/ProjectCard';
import CountryItem from '@/components/common/CountryItem';
import HfaCategoriesList from '@/components/common/list/HfaCategoriesList';
import DonorsList from '@/components/common/list/DonorsList';
import RegionItem from '@/components/common/RegionItem';
import CustomAnswersCell from '@/components/dashboard/CustomAnswersCell';
import GoalAreaItem from '@/components/dashboard/GoalAreaItem';
import ResultAreaItem from '@/components/dashboard/ResultAreaItem';
import CurrentPage from '@/components/dashboard/CurrentPage';
import FieldOfficeItem from '@/components/project/FieldOfficeItem';
import CapabilitiesList from '@/components/project/CapabilitiesList';
import { setTimeout } from 'timers';

export default {
  components: {
    ProjectCard,
    CountryItem,
    HfaCategoriesList,
    DonorsList,
    RegionItem,
    CustomAnswersCell,
    CurrentPage,
    FieldOfficeItem,
    CapabilitiesList,
    GoalAreaItem,
    ResultAreaItem
  },
  data () {
    return {
      pageSizeOption: [10, 20, 50, 100],
      tableMaxHeight: 200,
      localSort: null
    };
  },
  computed: {
    ...mapGetters({
      projectsList: 'dashboard/getProjectsList',
      selectedColumns: 'dashboard/getSelectedColumns',
      selectedRows: 'dashboard/getSelectedRows',
      selectAll: 'dashboard/getSelectAll',
      total: 'dashboard/getTotal',
      countryColumns: 'dashboard/getCountryColumns',
      donorColumns: 'dashboard/getDonorColumns',
      getCapabilityLevels: 'projects/getCapabilityLevels',
      getCapabilityCategories: 'projects/getCapabilityCategories',
      getCapabilitySubcategories: 'projects/getCapabilitySubcategories'
    }),
    ...mapGettersActions({
      pageSize: ['dashboard', 'getPageSize', 'setPageSize', 0],
      currentPage: ['dashboard', 'getCurrentPage', 'setCurrentPage', 0],
      sorting: ['dashboard', 'getSorting', 'setSorting', 0]
    }),
    paginationOrderStr () {
      const loc = this.$i18n.locale;
      return loc === 'ar' ? 'sizes, next, slot, prev' : 'sizes, prev, slot, next';
    }
  },
  watch: {
    selectAll: {
      immediate: true,
      handler (value) {
        if (this.$refs.mainTable) {
          this.$refs.mainTable.clearSelection();
          if (value) {
            this.$refs.mainTable.toggleAllSelection();
          }
        }
      }
    },
    selectedColumns: {
      immediate: false,
      handler (columns) {
        this.$nextTick(() => {
          this.$refs.mainTable.doLayout();
          setTimeout(() => {
            this.alignFixedTableWidthForRTL();
          }, 50);
        });
      }
    },
    sorting: {
      immediate: false,
      handler (current) {
        if (current !== this.localSort) {
          this.fixSorting(current);
        }
      }
    }
  },
  mounted () {
    setTimeout(() => {
      this.fixTableHeight();
      this.fixSorting(this.$route.query.ordering);
      if (this.selectAll) {
        this.$refs.mainTable.clearSelection();
        this.$refs.mainTable.toggleAllSelection();
      }
      this.$nextTick(() => {
        this.alignFixedTableWidthForRTL();
      });
    }, 500);
  },
  methods: {
    ...mapActions({
      setSelectedRows: 'dashboard/setSelectedRows'
    }),
    customHeaderRenderer (h, { column, $index }) {
      return h('span', { attrs: { title: column.label } }, column.label);
    },
    selectHandler (selection) {
      this.setSelectedRows(selection.map(s => s.id));
    },
    rowClassCalculator ({ row }) {
      return this.selectedRows.includes('row'.id) ? 'Selected' : 'NotSelected';
    },
    sortChanged ({ prop, order }) {
      if (order === 'descending') {
        this.sorting = '-' + prop;
        this.localSort = '-' + prop;
      } else {
        this.sorting = prop;
        this.localSort = prop;
      }
    },
    convertDate (date) {
      return date ? format(date, 'DD/MM/YYYY HH:mm') : 'N/A';
    },
    fixTableHeight () {
      const maxHeight = window.getComputedStyle(this.$el).getPropertyValue('max-height');
      this.tableMaxHeight = +maxHeight.replace('px', '');
      this.$refs.mainTable.doLayout();
    },
    fixSorting (prop) {
      if (prop) {
        let direction = 'ascending';
        if (prop.startsWith('-')) {
          direction = 'descending';
          prop = prop.replace('-', '');
        }
        this.$refs.mainTable.sort(prop, direction);
      }
    },
    alignFixedTableWidthForRTL () {
      const locale = this.$i18n.locale;
      if (locale === 'ar') {
        const rawTableWidth = document.querySelector('.el-table__header').offsetWidth;
        const fixedFieldWidths = 275;
        const toShowBorder = 1;

        const toAlignWidth = rawTableWidth - fixedFieldWidths - toShowBorder;

        const fixedTableHeader = document.querySelector('.el-table__fixed-header-wrapper');
        const fixedTableBody = document.querySelector('.el-table__fixed-body-wrapper');

        if (fixedTableBody && fixedTableHeader) {
          fixedTableHeader.style.left = -toAlignWidth + 'px';
          fixedTableBody.style.left = -toAlignWidth + 'px';
        }
      }
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .MainTable {
    margin: 0 40px;
    max-height: calc(100vh - @topBarHeightSubpage - @actionBarHeight - @tableTopActionsHeight - @appFooterHeight - 93px);

    // Custom table template
    .el-table {
      th, td {
        vertical-align: top;
      }

      th {
        > .cell {
          line-height: 24px;
          // truncate long headers
          white-space: nowrap;
          //
        }

        &.is-leaf {
          border-bottom-color: @colorTextMuted;
        }

        // Disable select-all-row
        &.el-table-column--selection {
          .el-checkbox {
            display: none;
          }
        }
      }

      td {
        > .cell {
          line-height: 17px;
          word-break: normal;

          p {
            position: relative;
            margin: 0;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            // With 17 in the calc the fixed columns and the rest of the table go out of sync
            max-height: calc(16.5px * 4);

            // &::after {
            //   content: "";
            //   text-align: right;
            //   position: absolute;
            //   bottom: 0;
            //   right: 0;
            //   width: 20%;
            //   height: 17px;
            //   background: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 1));
            // }

          }

          a {
            &[rel="email"] {
              display: block;
            }
          }
        }
      }

      // selected table row
      .el-table__row {
        &.Selected {
          > td {
            background-color: #FFFBDC;

            &.el-table-column--selection {
              box-shadow: inset 2px 0 0 #FBC02D;
            }
          }
        }
      }

      .el-table-column--selection {
        > .cell {
          text-overflow: clip !important;
        }
      }

      .caret-wrapper {
        position: absolute;
        top: 1px;
        right: 4px;
      }

      .el-table__empty-block {
        position: relative;
        width: 100% !important;
        text-align: center;

        .el-table__empty-text {
          width: auto;
          font-weight: 700;
        }
      }

      .ProjectCard {
        overflow: visible;

        .ProjectName {
          padding-right: 12px;
        }

        .ProjectCountryOrg {
          margin-top: 4px;
        }

        .ProjectLegend {
          top: 1px;
          right: -1px;
          opacity: 1 !important;

          .svg-inline--fa {
            position: relative;
            height: 14px;
            font-size: 12px;

            &.fa-star {
              right: 1px;
              font-size: 11px;
            }

            &.fa-globe-africa {
              right: 1px;
            }
          }
        }
      }

      .CountryItem {
        .CountryFlag {
          display: none;
        }

        .CountryName {
          margin: 0;
          font-size: @fontSizeSmall;
          line-height: inherit;
        }
      }

      .DonorList {
        ul {
          padding: 0;
          margin: 0;
        }

        .DonorItem {
          display: inline-flex;
          align-items: flex-start;
          width: 100%;

          .svg-inline--fa {
            position: relative;
            top: -1px;
            margin-right: 5px;
          }
        }
      }

      .HealthFocusAreasList,
      .CustomAnswersCell,
      .CapabilitiesList {
        ul {
          list-style-type: none;
          margin: 0;
          padding: 0;

          li {
            position: relative;

            > span {
              &:first-child {
                position: absolute;
                left: 0;
                top: 0;
              }

              &:last-child {
                display: block;
                padding-left: 15px;
                .textTruncate();
              }
            }
          }
        }
      }
    }

    .Pagination {
      z-index: 5;
      position: relative;
      top: -1px;
      width: 100%;
      // don't forget to calculate this into max-height of MainTable
      height: 53px;
      //
      box-sizing: border-box;
      border: solid @colorGrayLight;
      border-width: 1px 1px 2px;
      background-color: @colorBrandBlueLight;
      text-align: right;

      .el-pagination {
        padding: 11px 15px;
        font-weight: 400;

        .el-pagination__sizes {
          float: left;
          margin: 0;
        }

        .PageCounter {
          display: inline-block;
          margin: 0 10px;
          font-size: @fontSizeSmall;
          color: @colorTextSecondary;
        }

        button {
          padding: 0;
          background-color: transparent;
          transition: @transitionAll;

          &:hover {
            background-color: lighten(@colorBrandBlueLight, 3%);
          }

          i {
            font-size: @fontSizeLarge;
            font-weight: 700;
          }
        }
      }
    }
  }
</style>
