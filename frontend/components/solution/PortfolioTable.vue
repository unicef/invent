<template>
  <table class="SimpleTable">
    <thead>
      <tr>
        <th>Innovation Portfolio</th>
        <th>Public Statement(s)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Climate change</td>
        <td>2. Accessing ...</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {}
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
  td:nth-child(1) {
    width: 30%;
  }
}
</style>
