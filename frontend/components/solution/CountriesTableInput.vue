<template>
  <div>
    <table data-test="countries-table-input" class="SimpleTable">
      <thead>
        <tr>
          <th><translate>Country</translate></th>
          <th><translate>Region</translate></th>
          <th><translate>People Reached</translate></th>
          <th>&nbsp;</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in table" :key="row.id">
          <td>
            <CountrySelectSingle @change="() => updateRegion(row.id, row.country)" v-model.number="row.country" />
          </td>
          <td>{{ printRegionNameList(row.region) }}</td>
          <td>
            <el-input-number
              v-model="row.reached"
              v-validate="{}"
              data-vv-name="people_reached_per_country"
              data-vv-as="People reached per country"
              controls-position="right"
              :min="0"
              class="number-input"
            />
          </td>
          <td>
            <el-button type="text" class="IconLeft" @click="() => deleteRow(row.id)">
              <translate>Delete</translate>
            </el-button>
          </td>
        </tr>
      </tbody>
    </table>
    <el-button type="text" class="IconLeft" @click="addRow">
      <fa icon="plus" /> <translate>Add Country</translate>
    </el-button>
  </div>
</template>

<script>
import { uuidv4 } from '~/utilities/dom'
import CountrySelectSingle from '../common/CountrySelectSingle.vue'
import { mapGetters } from 'vuex'

export default {
  components: {
    CountrySelectSingle,
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
      getRegionsByCountry: 'countries/getRegionsByCountry',
      // regions: 'system/getRegions',
      getRegionDetails: 'system/getRegionDetails',
    }),
  },
  // mounted: function () {
  //   this.table = this.tableData
  // },
  watch: {
    tableData: function () {
      this.table = this.tableData
    },
  },
  methods: {
    addRow: function () {
      this.table = [...this.table, { id: uuidv4(), country: '', region: [], reached: 0 }]
      // this.emit('update-countries', this.table)
      //table actions-> table changed + new table
      // initial table = tableData comparison
      // when props update -> table actions cleanup
    },
    deleteRow: function (id) {
      this.table = this.table.filter((row) => row.id !== id)
    },
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
    updateRegion: function (recordId, countryId) {
      this.table = this.table.map((record) => {
        if (record.id !== recordId) {
          return record
        } else {
          return {
            id: record.id,
            country: countryId,
            region: this.getRegionsByCountry(countryId),
            reached: record.reached,
          }
        }
      })
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
  th:nth-child(1) {
    width: 30%;
  }
  th:nth-child(2) {
    width: 30%;
  }
  th:nth-child(3) {
    width: 30%;
  }
  tr:nth-child(even) {
    background-color: lightgrey;
  }
  .number-input {
    width: 90%;
    &.el-input-number .el-input__inner {
      text-align: left;
    }
  }
}
</style>
