<template>
  <div class="MainTable">
    <el-table
      ref="mainTable"
      :data="currentList"
      :max-height="tableMaxHeight"
      :row-class-name="'NotSelected'"
      :stripe="false"
      :border="true"
      @sort-change="sortTable"
    >
      <!-- <el-table-column :resizable="false" type="selection" align="center" width="45" class-name="selection-td" /> -->
      <el-table-column
        :resizable="false"
        :label="$gettext('Solution name') | translate"
        sortable="custom"
        prop="name"
        width="280"
        class-name="project-td"
      >
        <template slot-scope="scope">
          <nuxt-link
            class="ProjectName"
            :to="
              localePath({
                name: 'organisation-solutions-id',
                params: { id: scope.row.id },
                query: { portfolio: $route.params.id },
              })
            "
            >{{ scope.row.name }}</nuxt-link
          >
        </template>
      </el-table-column>
      <el-table-column :resizable="false" :label="$gettext('Portfolios') | translate" min-width="200">
        <template slot-scope="scope">
          <p>
            {{
              scope.row.portfolios
                .map((portfolio, index) => (index === 0 ? portfolio.name : ` ${portfolio.name}`))
                .toString()
            }}
          </p>
        </template>
      </el-table-column>
      <el-table-column :resizable="false" :label="$gettext('Problem statement') | translate" min-width="300">
        <template slot-scope="scope">
          <div v-if="scope.row.portfolios.length > 1">
            <div v-for="ps in scope.row.problem_statements">
              <p>{{ ps.portfolio_name ? `${ps.portfolio_name}: ${ps.name}` : ps.name }}</p>
            </div>
          </div>
          <div v-else>
            <div v-for="ps in scope.row.problem_statements">
              <p>{{ ps.name }}</p>
            </div>
          </div>
        </template>
      </el-table-column>

      <el-table-column
        sortable="custom"
        :resizable="false"
        :label="$gettext('Phase') | translate"
        prop="phase_name"
        width="180"
      >
        <template slot-scope="scope"
          ><p>{{ scope.row.phase_name }}</p></template
        >
      </el-table-column>

      <el-table-column
        sortable="custom"
        :resizable="false"
        :label="$gettext('Reach') | translate"
        width="180"
        prop="people_reached"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.people_reached }}</p>
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
import { mapGetters } from 'vuex'

import CurrentPage from '@/components/dashboard/CurrentPage'

export default {
  components: {
    CurrentPage,
  },
  data() {
    return {
      pageSizeOption: [10, 20, 50, 100],
      tableMaxHeight: 240,
      addFavoriteText: this.$gettext('Add to Favorites'),
      removeFavoriteText: this.$gettext('Remove from Favorites'),
      pageSize: 10,
      currentPage: 1,
      table: [],
    }
  },
  computed: {
    ...mapGetters({
      getAllActiveSolutionsList: 'solutions/getAllActiveSolutionsList',
    }),
    total() {
      return this.table.length + 1
    },
    showPagination() {
      return this.total > 10
    },
    currentList() {
      const start = this.pageSize * (this.currentPage - 1)
      const end = this.pageSize * this.currentPage
      return this.table.slice(start, end)
    },

    paginationOrderStr() {
      const loc = this.$i18n.locale
      return loc === 'ar' ? 'sizes, next, slot, prev' : 'sizes, prev, slot, next'
    },
  },
  watch: {
    getAllActiveSolutionsList() {
      this.currentOrderedList()
      this.$nextTick(() => {
        this.sortTable({ prop: 'name', order: 'ascending' })
      })
    },
  },
  mounted() {
    this.currentOrderedList()
    this.$nextTick(() => {
      this.sortTable({ prop: 'name', order: 'ascending' })
    })
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
    currentOrderedList() {
      let ctable = JSON.parse(JSON.stringify(this.getAllActiveSolutionsList))
      this.table = ctable.map((solution) => {
        const problem_statements = solution.problem_statements.sort((a, b) =>
          a.portfolio_name.localeCompare(b.portfolio_name, this.$i18n.locale, { numeric: true })
        )
        return { ...solution, problem_statements }
      })
    },
    sortTable({ column, prop, order }) {
      const solutionsList = this.table
      if (order === 'ascending') {
        this.table = solutionsList.sort((a, b) =>
          a[prop].toString().localeCompare(b[prop].toString(), this.$i18n.locale, { numeric: true })
        )
      } else if (order === 'descending') {
        this.table = solutionsList.sort((a, b) =>
          b[prop].toString().localeCompare(a[prop].toString(), this.$i18n.locale, { numeric: true })
        )
      }
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
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.MainTable {
  margin: 0 40px 120px;
  max-height: calc(100vh - @topBarHeightSubpage - @actionBarHeight - @tableTopActionsHeight - 93px);

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

      border-left: 1px solid @colorBrandGrayLight !important;

      .el-table__empty-text {
        width: auto;
        font-weight: 700;
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
