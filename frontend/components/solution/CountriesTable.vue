<template>
  <table data-test="countries-table" class="SimpleTable">
    <thead>
      <tr>
        <th><translate>Country</translate></th>
        <th><translate>Region</translate></th>
        <th><translate>People Reached</translate></th>
      </tr>
    </thead>
    <tbody v-if="!!tableData.length">
      <tr v-for="row in sortedCountriesTable" :key="row.id">
        <td>{{ row.country }}</td>
        <td>{{ row.region }}</td>
        <td>{{ row.people_reached }}</td>
      </tr>
    </tbody>
    <tbody v-else>
      <tr>
        <td><translate>No data</translate></td>
        <td><translate>No data</translate></td>
        <td><translate>No data</translate></td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  props: {
    tableData: {
      type: Array,
    },
  },
  computed: {
    ...mapGetters({
      getRegionDetails: 'system/getRegionDetails',
      countries: 'countries/getCountries',
    }),
    sortedCountriesTable() {
      const namedTable = this.tableData.map((row) => ({
        id: row.id,
        country: this.getCountryName(row.country),
        region: this.printRegionName(row.region),
        people_reached: row.people_reached,
      }))

      return namedTable.sort((a, b) => {
        const res = a.country.localeCompare(b.country, this.$i18n.locale)
        if (res > 0) {
          return 1
        } else if (res < 0) {
          return -1
        } else {
          return 0
        }
      })
    },
  },
  methods: {
    printRegionName: function (regionId) {
      if (regionId === null || regionId === undefined) {
        return 'N/A'
      } else {
        return this.getRegionDetails(regionId).name
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
