<template>
  <div>
    <input v-show="false" ref="fileInput" type="file" @change="setCsv" />
    <el-button
      :loading="csvProcessing"
      type="text"
      class="IconLeft"
      @click="triggerFile"
    >
      <fa icon="plus" /> <translate>Select Facility List</translate>
    </el-button>

    <template v-if="dataReady">
      <div class="FacilityList">
        <h5>
          <translate :parameters="{ num: simpleFacilities.length }">
            Imported Facilities ({num}):
          </translate>
        </h5>
        <ul v-for="facility in simpleFacilities" :key="facility">
          <li>
            <fa icon="building" />
            {{ facility }}
          </li>
        </ul>
      </div>
    </template>
  </div>
</template>

<script>
import Papa from 'papaparse'
import { mapGettersActions } from '../../utilities/form'

export default {
  name: 'FacilityImport',
  props: {
    places: {
      type: Array,
      default: () => [],
    },
    initialData: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      showMatched: false,
      showNotMatched: true,
      csvProcessing: false,
    }
  },
  computed: {
    ...mapGettersActions({
      facilities: ['admin/map', 'getFacilities', 'setFacilities'],
    }),
    dataReady() {
      return this.facilities && this.facilities.length > 0
    },
    simpleFacilities() {
      return this.facilities.map((f) => f.name)
    },
  },
  watch: {
    initialData: {
      immediate: true,
      handler(data) {
        if (data && data.length > 0) {
          this.facilities = data.map((d) => ({ name: d }))
        }
      },
    },
  },
  methods: {
    triggerFile() {
      this.csvProcessing = true
      this.$refs.fileInput.click()
    },
    setCsv(event) {
      const file = event.target.files ? event.target.files[0] : null
      Papa.parse(file, {
        header: true,
        complete: (result) => {
          this.facilities = result.data.map((f) => ({
            name: f.name || f.Name || f.NAME,
            place: f.county || f.County || f.COUNTY,
          }))
          this.csvProcessing = false
        },
      })
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.FacilityList {
  ul {
    list-style-type: none;
    margin: 0;
    padding: 0;

    li {
      position: relative;
      font-size: @fontSizeBase;
      margin: 0 0 10px;
      padding: 0 20px;
      color: @colorBrandPrimary;
      cursor: pointer;
      transition: @transitionAll;

      &:hover {
        color: @colorBrandPrimaryLight;
      }

      .svg-inline--fa {
        position: absolute;
        top: 0;
        left: 0;
        width: 14px;
      }
    }
  }
}
</style>
