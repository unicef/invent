<template>
  <table class="SimpleTable">
    <thead>
      <tr>
        <th>Innovation Portfolio</th>
        <th>Public Statement(s)</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in tableData" :key="row.id">
        <td>{{ row.portfolio }}</td>
        <td>{{ publicStatements(row.publicStatements) }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  props: {
    tableData: [],
  },
  methods: {
    publicStatements: function (statementsArray) {
      return statementsArray.toString()
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
