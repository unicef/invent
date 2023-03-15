<template>
  <table data-test="portfolio-table" class="SimpleTable">
    <thead>
      <tr>
        <th><translate>Innovation Portfolio</translate></th>
        <th><translate>Problem Statements</translate></th>
      </tr>
    </thead>
    <tbody>
      <tr v-if="!portfoliosProblemStatements.length > 0">
        <td>None</td>
        <td>None</td>
      </tr>
      <tr v-else v-for="row in portfoliosProblemStatements">
        <td>{{ portfolio(row.portfolio_id) }}</td>
        <td>{{ statements(row.problem_statements) }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  props: {
    portfoliosProblemStatements: Array,
  },
  computed: {
    ...mapGetters({
      getPortfolios: 'solution/getPortfoliosList',
      getStatements: 'solution/getProblemStatementList',
    }),
  },
  methods: {
    statements: function (statementsArray) {
      const st = statementsArray
        .map((statementId) => this.getStatements.find((statement) => statement.id === statementId).name)
        .toString()
      return st === '' ? 'None' : st
    },
    portfolio: function (portfolioId) {
      // return 22222
      return this.getPortfolios.find((portfolio) => portfolio.id === portfolioId).name
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
      padding: 4px 0px 4px 10px;
    }
  }
  td {
    padding: 4px 0px 4px 10px;
  }
  td:nth-child(1) {
    width: 30%;
  }
}
</style>
