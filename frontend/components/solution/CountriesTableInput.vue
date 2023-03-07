<template>
  <div>
    <table class="SimpleTable">
      <thead>
        <tr>
          <th>Country</th>
          <th>Region</th>
          <th>People Reached</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Croatia</td>
          <td>ECAR</td>
          <td>120</td>
          <td>
            <el-button type="text" class="IconLeft"> <translate>Delete</translate> </el-button>
          </td>
        </tr>
        <tr>
          <td>Croatia</td>
          <td>ECAR</td>
          <td>120</td>
          <td>
            <el-button type="text" class="IconLeft"> <translate>Delete</translate> </el-button>
          </td>
        </tr>
      </tbody>
    </table>
    <el-button type="text" class="IconLeft"> <fa icon="plus" /> <translate>Add Country</translate> </el-button>
  </div>
</template>

<script>
export default {
  props: {
    tableData: [],
  },
  data: function () {
    return {
      table: [],
      tableActions: [],
    }
  },
  methods: {
    addRow: function () {
      this.table = [...this.table, { action: '', id: '', country: '', region: '', people_reached: '' }]
      this.tableActions.push({ action: 'add', data: { id: '', country: '', region: '', people_reached: '' } })
      this.emit('update-countries', this.table)
      //table actions-> table changed + new table
      // initial table = tableData comparison
      // when props update -> table actions cleanup
    },
  },
}
</script>

<style lang="less">
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
  td:nth-child(2) {
    width: 30%;
  }
  td:nth-child(3) {
    width: 30%;
  }
  tr:nth-child(even) {
    background-color: lightgrey;
  }
}
</style>
