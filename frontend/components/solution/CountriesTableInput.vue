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
        <tr v-for="row in tableData" :key="row.row_id">
          <td>
            <CountrySelectDisabledSingle
              @change="() => updateRegion(row.row_id, row.country)"
              v-model.number="row.country"
              :selectedCountries="tableData"
              v-validate="rules.countrySingleSelect"
              name="country-single-select"
            />
          </td>
          <td>{{ getRegionName(row.region) }}</td>
          <td>
            <el-input-number
              v-model="row.people_reached"
              v-validate="rules.countrySingleNumber"
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
    <p v-show="errors.first('country-single-select')" class="error">
      <translate>Country, cannot be empty.</translate>
    </p>
    <el-button type="text" class="IconLeft" @click="addRow">
      <fa icon="plus" /> <translate>Add Country</translate>
    </el-button>
  </div>
</template>

<script>
import { uuidv4 } from '~/utilities/dom'
import VeeValidationMixin from '@/components/mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '@/components/mixins/ProjectFieldsetMixin.js'
import CountrySelectDisabledSingle from './CountrySelectDisabledSingle.vue'
import { mapGetters } from 'vuex'

export default {
  components: {
    CountrySelectDisabledSingle,
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  model: {
    prop: 'tableData',
    event: 'change',
  },
  props: {
    tableData: Array,
    rules: { type: Object, default: {} },
    publishRules: {},
    draftRules: {},
    apiErrors: {},
  },
  $_veeValidate: {
    value() {
      return this.tableData
    },
    //  rejectsFalse: true,
  },
  computed: {
    ...mapGetters({
      getRegionsByCountry: 'countries/getRegionsByCountry',
      getRegionDetails: 'system/getRegionDetails',
    }),
  },
  methods: {
    addRow: function () {
      const newTable = [
        ...this.tableData,
        { row_id: uuidv4(), id: null, country: null, region: null, people_reached: 0 },
      ]
      this.$emit('change', newTable)
    },
    deleteRow: function (id) {
      const newTable = this.tableData.filter((row) => row.id !== id)
      this.$emit('change', newTable)
    },
    getRegionName: function (regionId) {
      if (regionId === null) {
        return this.$gettext('N/A')
      } else {
        const regName = this.getRegionDetails(regionId).name
        console.log(regName)
        return regName
      }
    },
    // printRegionNameList: function (regionArray) {
    //   if (!regionArray || !regionArray.length > 0) {
    //     return 'N/A'
    //   } else {
    //     return regionArray.map((regionRec) => this.getRegionName(regionRec)).toString()
    //   }
    // },
    updateRegion: function (recordId, countryId) {
      const newTable = this.tableData.map((record) => {
        if (record.row_id !== recordId) {
          return record
        } else {
          return {
            row_id: record.row_id,
            id: record.id,
            country: countryId,
            region: this.getRegionsByCountry(countryId)[0],
            people_reached: record.people_reached,
          }
        }
      })

      this.$emit('change', newTable)
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
    width: 40%;
  }
  th:nth-child(2) {
    width: 20%;
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
.error {
  color: red;
  font-size: @fontSizeBase;
}
</style>
