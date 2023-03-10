<template>
  <table data-test="portfolio-table" class="SimpleTable">
    <thead>
      <tr>
        <th><translate>Innovation Portfolio</translate></th>
        <th><translate>Problem Statements</translate></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>{{ portfolios(innovationPortfolios) }}</td>
        <td>{{ statements(problemStatements) }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  props: {
    innovationPortfolios: Array,
    problemStatements: Array,
  },
  computed: {
    ...mapGetters({
      getPortfolios: 'solution/getPorfoliosList',
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
    portfolios: function (portfolioArray) {
      const st = portfolioArray
        .map((portId) => this.getPortfolios.find((portfolio) => portfolio.id === portId).name)
        .toString()
      return st === '' ? 'None' : st
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
