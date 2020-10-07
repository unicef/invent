<template>
  <div class="ProjectApprovalTable">
    <el-row type="flex" class="Actions">
      <el-col class="Download">
        <el-button
          :disabled="rowSelection.length === 0"
          class="IconLeft"
          @click="csvExport"
        >
          <fa icon="download" />
          <translate>Export Selected</translate>
        </el-button>
      </el-col>
      <el-col class="Filters">
        <el-row type="flex">
          <el-col>
            <div class="Separator" />
          </el-col>
          <el-col>
            <span class="Label"> Approved: </span>
          </el-col>
          <el-col>
            <el-checkbox-group v-model="filters">
              <el-checkbox :label="true" border size="small"> Yes </el-checkbox>
              <el-checkbox :label="false" border size="small"> No </el-checkbox>
              <el-checkbox :label="null" border size="small">
                Pending
              </el-checkbox>
            </el-checkbox-group>
          </el-col>
        </el-row>
      </el-col>
    </el-row>

    <el-table
      :data="filteredList"
      size="medium"
      @selection-change="selectionHandler"
    >
      <el-table-column type="selection" align="center" width="46" />

      <el-table-column
        :label="$gettext('Initiative') | translate"
        sortable
        prop="project_name"
        class-name="ProjectName"
      />
      <el-table-column
        :label="$gettext('User') | translate"
        sortable
        width="220px"
        prop="user"
      >
        <template slot-scope="scope">
          <user-item :id="getUserId(scope.row)" show-organisation />
        </template>
      </el-table-column>
      <el-table-column
        :label="$gettext('Approved') | translate"
        sortable
        width="120px"
        prop="approved"
      >
        <template slot-scope="scope">
          <approval-tag :value="scope.row.approved" />
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="120px">
        <template slot-scope="scope">
          <el-button size="mini" @click="openDetails(scope.row.id)">
            Details
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import Papa from 'papaparse'
import { format } from 'date-fns'
import { mapGetters, mapActions } from 'vuex'
import { uriDownloader } from '../../utilities/dom'
import UserItem from '../common/UserItem'
import ApprovalTag from './ApprovalTag'

export default {
  components: {
    ApprovalTag,
    UserItem,
  },
  data() {
    return {
      filters: [true, false, null],
      rowSelection: [],
    }
  },
  computed: {
    ...mapGetters({
      list: 'admin/approval/getList',
      getUserDetails: 'system/getUserProfileDetails',
    }),
    filteredList() {
      return this.list.filter(
        (i) =>
          this.filters.length === 0 ||
          this.filters.some((f) => f === i.approved)
      )
    },
    parsedList() {
      return this.rowSelection.map((i) => {
        const user = this.getUserDetails(this.getUserId(i))
        const approved =
          i.approved === true
            ? this.$gettext('Yes')
            : i.approved === false
            ? this.$gettext('No')
            : this.$gettext('Pending')
        return {
          project_id: i.project,
          project_name: i.project_name,
          user: user ? user.name : '',
          approved,
          modified: format(i.modified, 'YYYY-MM-DD HH:mm'),
        }
      })
    },
  },
  methods: {
    ...mapActions({
      openDetails: 'admin/approval/setCurrentElement',
    }),
    getUserId(row) {
      const history = row.history
      if (history && history.length > 0) {
        const first = history[0]
        if (first && first.history_user__userprofile) {
          return first.history_user__userprofile
        }
        return row.legacy_approved_by
      }
    },
    filterHandler(value, row, column) {
      const property = column.property
      return row[property] === value
    },
    selectionHandler(selection) {
      this.rowSelection = selection
    },
    csvExport() {
      const csv = Papa.unparse(this.parsedList, { delimiter: ';' })
      const toDownload = `data:text/csv;charset=utf-8,${csv}`
      uriDownloader(toDownload, 'project-approval-export.csv')
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.ProjectApprovalTable {
  .Actions {
    margin: 0 0 20px;

    .Download {
      width: auto;
    }

    .Filters {
      width: 100%;

      .Label {
        font-size: @fontSizeBase;
        line-height: 38px;
      }

      .el-checkbox-group {
        display: inline-block;
        width: auto;
        margin: 4px 20px;
      }

      .Separator {
        .SeparatorStyle();
        display: inline-block;
        height: 38px;
        margin: 0 20px;
      }

      > .el-row {
        .el-col {
          width: auto;

          &:last-child {
            width: 100%;
          }
        }
      }
    }
  }

  .el-table {
    th,
    td {
      // vertical-align: top;
    }

    td {
      > .cell {
        line-height: 19px;
        word-break: normal;
      }
    }

    .ProjectName {
      padding-right: 80px;
      font-weight: 700;
    }
  }
}
</style>
