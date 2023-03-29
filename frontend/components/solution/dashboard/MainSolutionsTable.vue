<template>
  <div class="MainTable">
    <el-table
      ref="mainTable"
      :data="currentList"
      :max-height="tableMaxHeight"
      :row-class-name="rowClassCalculator"
      :stripe="false"
      :border="true"
      size="mini"
      style="width: inherit"
      :defalt-sort="{ prop: 'name', order: 'ascending' }"
    >
      <!-- <el-table-column :resizable="false" type="selection" align="center" width="45" class-name="selection-td" /> -->
      <el-table-column
        :resizable="false"
        :label="$gettext('Solution Name') | translate"
        prop="name"
        width="280"
        class-name="project-td"
      >
        <template slot-scope="scope">
          <nuxt-link
            class="ProjectName"
            :to="
              localePath({
                name: 'organisation-portfolio-innovation-solutions-id',
                params: { id: scope.row.id },
                query: { project: $route.params.id },
              })
            "
            >{{ scope.row.name }}</nuxt-link
          >
        </template>
      </el-table-column>

      <el-table-column
        :resizable="false"
        :label="$gettext('Problem Statement') | translate"
        style="{minWidth: 600px, maxWidth: 800px}"
      >
        <template slot-scope="scope">
          <ul v-for="ps in scope.row.problemStatements">
            <li>{{ ps.name }}</li>
          </ul>
        </template>
      </el-table-column>

      <el-table-column :resizable="false" :label="$gettext('Phase') | translate" prop="phase" width="180">
        <template slot-scope="scope"> {{ scope.row.phase }} </template>
      </el-table-column>

      <el-table-column :resizable="false" :label="$gettext('Reach') | translate" width="180" prop="reach">
        <template slot-scope="scope">
          <p>{{ scope.row.reach | formatNumber }}</p>
        </template>
      </el-table-column>
      <!-- new table fields -->
    </el-table>
    <div class="Pagination" v-show="showPagination">
      <el-pagination
        :current-page.sync="currentPage"
        :page-size.sync="pageSize"
        :page-sizes="pageSizeOption"
        :total="total"
        :layout="paginationOrderStr"
      >
        <current-page :total="total" :page-size="pageSize" :page="currentPage" />
      </el-pagination>
    </div>
  </div>
</template>

<script>
import { setTimeout } from 'timers'
import { format } from 'date-fns'
import { mapGetters, mapActions, mapState, mapMutations } from 'vuex'
import CurrentPage from '@/components/dashboard/CurrentPage'

export default {
  components: {
    CurrentPage,
  },
  data() {
    return {
      pageSizeOption: [10, 20, 50, 100],
      tableMaxHeight: 200,
      localSort: null,
      addFavoriteText: this.$gettext('Add to Favorites'),
      removeFavoriteText: this.$gettext('Remove from Favorites'),
      pageSize: 10,
      currentPage: 1,
    }
  },
  computed: {
    ...mapState({
      tab: (state) => state.portfolio.tab,
    }),
    ...mapGetters({
      selectedColumns: 'dashboard/getSelectedColumns',
      selectedRows: 'portfolio/getSelectedRows',
      selectAll: 'portfolio/getSelectAll',
      getSolutionsList: 'solutions/getSolutionsList',
      getPortfoliosList: 'solution/getPortfoliosList',
    }),
    total() {
      return this.getSolutionsList.length + 1
    },
    showPagination() {
      return this.total > 10
    },
    currentList() {
      const start = this.pageSize * (this.currentPage - 1)
      const end = this.pageSize * this.currentPage
      return this.getSolutionsList.slice(start, end)
    },
    paginationOrderStr() {
      const loc = this.$i18n.locale
      return loc === 'ar' ? 'sizes, next, slot, prev' : 'sizes, prev, slot, next'
    },
  },
  watch: {
    selectAll: {
      immediate: true,
      handler(value) {
        if (this.$refs.mainTable) {
          if (value) {
            this.$refs.mainTable.toggleAllSelection()
          } else if (this.selectedRows.length === 0) {
            this.$refs.mainTable.clearSelection()
          }
        }
      },
    },
    selectedColumns: {
      immediate: false,
      handler(columns) {
        this.$nextTick(() => {
          this.$refs.mainTable.doLayout()
          setTimeout(() => {
            this.alignFixedTableWidthForRTL()
          }, 50)
        })
      },
    },
    sorting: {
      immediate: false,
      handler(current) {
        if (current !== this.localSort) {
          this.fixSorting(current)
        }
      },
    },
  },
  mounted() {
    setTimeout(() => {
      this.fixTableHeight()
      this.fixSorting(this.$route.query.ordering)
      if (this.selectAll) {
        this.$refs.mainTable.clearSelection()
        this.$refs.mainTable.toggleAllSelection()
      }
      this.$nextTick(() => {
        this.alignFixedTableWidthForRTL()
      })
    }, 500)
  },
  methods: {
    ...mapMutations({
      setSearch: 'search/SET_SEARCH',
      setPageSize: 'search/setPageSize',
    }),
    ...mapActions({
      setSelectedRows: 'portfolio/setSelectedRows',
      addFavorite: 'projects/addFavorite',
      removeFavorite: 'projects/removeFavorite',

      loadProblemPortfoliolists: 'solution/loadProblemPortfoliolists',
    }),

    rowClassCalculator({ row }) {
      return this.selectedRows.includes(row.id) ? 'Selected' : 'NotSelected'
    },

    convertDate(date) {
      return date ? format(date, 'DD/MM/YYYY HH:mm') : ' ' // N/A
    },
    fixTableHeight() {
      const maxHeight = window.getComputedStyle(this.$el).getPropertyValue('max-height')
      this.tableMaxHeight = +maxHeight.replace('px', '')
      this.$refs.mainTable.doLayout()
    },
    fixSorting(prop) {
      if (prop) {
        let direction = 'ascending'
        if (prop.startsWith('-')) {
          direction = 'descending'
          prop = prop.replace('-', '')
        }
        this.$refs.mainTable.sort(prop, direction)
      }
    },
    alignFixedTableWidthForRTL() {
      const locale = this.$i18n.locale
      if (locale === 'ar') {
        const rawTableWidth = document.querySelector('.el-table__header').offsetWidth
        const fixedFieldWidths = 275
        const toShowBorder = 1

        const toAlignWidth = rawTableWidth - fixedFieldWidths - toShowBorder

        const fixedTableHeader = document.querySelector('.el-table__fixed-header-wrapper')
        const fixedTableBody = document.querySelector('.el-table__fixed-body-wrapper')

        if (fixedTableBody && fixedTableHeader) {
          fixedTableHeader.style.left = -toAlignWidth + 'px'
          fixedTableBody.style.left = -toAlignWidth + 'px'
        }
      }
    },

    handleFavorite(id) {
      console.log(`this will mark or unmark ${id}`)
    },
    sizeChange(val) {
      this.setPageSize(val)
    },
    pagClick(val) {
      this.setSearch({ key: 'page', val })
    },
    stageIDs(stageList) {
      return stageList ? stageList.map((stage) => stage.id) : []
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.MainTable {
  margin: 0 40px 120px;
  max-height: calc(100vh - @topBarHeightSubpage - @actionBarHeight - @tableTopActionsHeight - @appFooterHeight - 93px);

  .favorite {
    cursor: pointer;
    position: absolute;
    top: 32px;
    left: -30px;
    svg {
      font-size: 14px;
    }
    .heart-full {
      color: #c4225f;
    }
    .heart-empty {
      color: @colorBrandGrayLight;
    }
  }

  .el-table--border th {
    border-right: 1px solid @colorWhite;
  }
  .el-table--group,
  .el-table--border {
    border: 0px solid transparent;
  }
  .el-table__body {
    td:nth-child(1) {
      border-left: 1px solid @colorBrandGrayLight;
    }
  }

  .el-table__body tr.hover-row > td,
  .el-table__body tr.hover-row.current-row > td {
    background-color: #e8f6fd;
  }
  // Custom table template
  .el-table {
    th,
    td {
      vertical-align: top;
    }

    .caret-wrapper .sort-caret {
      &.ascending {
        border-bottom-color: @colorWhite;
      }
      &.descending {
        border-top-color: @colorWhite;
      }
    }

    th {
      background-color: @colorBrandPrimary;
      > .cell {
        font-size: @fontSizeSmall;
        color: @colorWhite;
        font-weight: bold;
        letter-spacing: 0;
        line-height: 29px;
        white-space: nowrap;
      }

      &.is-leaf {
        border-bottom-color: @colorWhite;
      }

      // Disable select-all-row
      &.el-table-column--selection {
        .el-checkbox {
          display: none;
        }
      }
    }

    td {
      padding: 10px 16px 10px 12px;
      &.selection-td {
        padding: 10px 0 10px 0 !important;
      }
      &.project-td {
        padding: 10px 10px 10px 12px;
      }
      > .cell {
        min-height: 37px;
        line-height: 17px;
        word-break: normal;
        padding: 0;
        p {
          position: relative;
          margin: 0;
          display: -webkit-box;
          -webkit-line-clamp: 4;
          -webkit-box-orient: vertical;
          // With 17 in the calc the fixed columns and the rest of the table go out of sync
          // max-height: calc(16.5px * 4);
          // but it should be 15, based on the line-height
          max-height: calc(15px * 4);
          font-size: @fontSizeSmall;
          letter-spacing: 0;
          line-height: 15px;
          font-weight: 100;
        }

        a {
          &[rel='email'] {
            display: block;
          }
        }
      }
    }

    // selected table row
    .el-table__row {
      &.Selected {
        > td {
          background-color: #e8f6fd;
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
      top: 4px;
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

    .CountryName {
      margin: 0;
      font-size: @fontSizeSmall;
      letter-spacing: 0;
      line-height: 15px;
      font-weight: 100;
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
    border-top: 1px solid @colorGrayLight;
    background-color: @colorWhite;
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
        letter-spacing: 0;
        line-height: 15px;
      }

      button {
        padding: 0;
        background-color: transparent;
        transition: @transitionAll;
        i {
          font-size: @fontSizeLarge;
          font-weight: 700;
        }
      }
    }
  }
  .ProjectName {
    color: @colorBrandPrimary;
    font-size: @fontSizeSmall;
    font-weight: bold;
    letter-spacing: 0;
    line-height: 16px;
    text-decoration: none;
  }
}
</style>
