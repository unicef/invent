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
      <tr v-for="row in tableData" :key="row.id">
        <td>{{ getCountryName(row.country) }}</td>
        <td>{{ printRegionNameList(row.region) }}</td>
        <td>{{ row.peopleReached }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  props: {
    tableData: [],
  },
  computed: {
    ...mapGetters({
      getRegionDetails: 'system/getRegionDetails',
      countries: 'countries/getCountries',
    }),
  },
  methods: {
    getRegionName: function (regionId) {
      return this.getRegionDetails(regionId).name
    },
    printRegionNameList: function (regionArray) {
      if (!regionArray || !regionArray.length > 0) {
        return 'N/A'
      } else {
        return regionArray.map((regionRec) => this.getRegionName(regionRec)).toString()
      }
    },
    getCountryName: function (id) {
      return this.countries.filter((country) => country.id === id)[0].name
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
