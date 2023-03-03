<template>
  <table class="SimpleTable">
    <thead>
      <tr>
        <th>Country</th>
        <th>Region</th>
        <th>People Reached</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Croatia</td>
        <td>ECAR</td>
        <td>120</td>
      </tr>
      <tr>
        <td>Croatia</td>
        <td>ECAR</td>
        <td>120</td>
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
    width: 40%;
  }
  td:nth-child(2) {
    width: 30%;
  }
  td:nth-child(3) {
    width: 30%;
  }
}
</style>
