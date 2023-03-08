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
      table: [
        { id: '21', country: 58, region: [0], reached: 1234 },
        { id: '2', country: 79, region: [1, 3], reached: 456 },
        { id: '3', country: 79, region: [], reached: 456 },
      ],
      tableActions: [],
    }
  },
  computed: {
    ...mapGetters({
      getRegionsByCountry: 'countries/getRegionsByCountry',
      // regions: 'system/getRegions',
      getRegionDetails: 'system/getRegionDetails',
    }),
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
      console.log(regionArray)
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
  .number-input {
    width: 90%;
    &.el-input-number .el-input__inner {
      text-align: left;
    }
  }
}
</style>
