<template>
  <div>
    <table data-test="portfolio-table-input" class="SimpleTable">
      <thead>
        <tr>
          <th><translate>Innovation Portfolio</translate></th>
          <th><translate>Problem Statements</translate></th>
          <th>&nbsp;</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in table" :key="row.portfolio_id">
          <td>
            <PortfolioSelectSingle @change="() => {}" v-model.number="row.portfolio_id" :portfoliosList="table" />
          </td>
          <td>
            <ProblemStatementsSelector :tableData="row.problem_statements" :portfolio="row.portfolio_id" />
          </td>
          <td>
            <el-button type="text" class="IconLeft" @click="() => deleteRow(row.portfolio_id)">
              <translate>Delete</translate>
            </el-button>
          </td>
        </tr>
      </tbody>
    </table>
    <el-button type="text" class="IconLeft" @click="addRow">
      <fa icon="plus" /> <translate>Add Portfolio</translate>
    </el-button>
  </div>
</template>

<script>
import PortfolioSelectSingle from './PortfolioSelectSingle.vue'
import { mapGetters } from 'vuex'
import ProblemStatementsSelector from './ProblemStatementsSelector.vue'

export default {
  components: {
    PortfolioSelectSingle,
    ProblemStatementsSelector,
  },
  props: {
    tableData: [],
  },
  data: function () {
    return {
      table: [],
    }
  },
  computed: {
    ...mapGetters({
      getPortfolios: 'solution/getPorfoliosList',
      getStatements: 'solution/getProblemStatementList',
    }),
  },
  watch: {
    tableData: function () {
      this.table = this.tableData
    },
  },
  methods: {
    addRow: function () {
      this.table = [...this.table, { portfolio_id: null, problem_statements: [] }]
      // this.emit('update-countries', this.table)
      //table actions-> table changed + new table
      // initial table = tableData comparison
      // when props update -> table actions cleanup
    },
    deleteRow: function (id) {
      this.table = this.table.filter((row) => row.portfolio_id !== id)
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.SimpleTable {
  width: 100%;
  box-sizing: border-box;
  border-collapse: collapse;
  thead {
    background-color: gray;
    color: white;
    text-align: left;

    th {
      padding-left: 10px;
    }
  }
  td {
    padding-left: 10px;
  }
  th:nth-child(1) {
    width: 30%;
  }
  th:nth-child(2) {
    width: 60%;
  }
  th:nth-child(3) {
    width: 10%;
  }
  tr:nth-child(even) {
    background-color: lightgrey;
  }
}
</style>
