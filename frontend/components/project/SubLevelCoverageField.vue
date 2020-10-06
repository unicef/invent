<template>
  <div class="SubNationalCoverageField">
    <simple-field v-if="countrySubLevelNames.first" class="FirstSubLevel">
      <div slot="header">
        <fa icon="map-marker" />
        <translate :parameters="{ name: countrySubLevelNames.first }">
          {name} level deployment
        </translate>
      </div>
      <el-row v-for="cov in coverage" :key="cov" type="flex">
        <el-col :span="24">
          <sub-level-item
            :level-name="countrySubLevelNames.first"
            :coverage="cov"
            :coverage-data="coverageData"
            :sub-levels="countryFirstSubLevel"
          />
        </el-col>
      </el-row>
    </simple-field>

    <simple-field v-if="countrySubLevelNames.second" class="SecondSubLevel">
      <div slot="header">
        <fa icon="map-marker" />
        <translate :parameters="{ name: countrySubLevelNames.second }">
          {name} level deployment
        </translate>
      </div>
      <el-row v-for="cov in coverageSecondLevel" :key="cov" type="flex">
        <el-col :span="24">
          <sub-level-item
            :level-name="countrySubLevelNames.second"
            :coverage="cov"
            :coverage-data="coverageData"
            :sub-levels="countrySecondSubLevel"
          />
        </el-col>
      </el-row>
    </simple-field>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

import SubLevelItem from './SubLevelItem'
import SimpleField from './SimpleField'

export default {
  components: {
    SubLevelItem,
    SimpleField,
  },
  props: {
    coverage: {
      type: Array,
      default: () => [],
    },
    coverageSecondLevel: {
      type: Array,
      default: () => [],
    },
    coverageData: {
      type: Object,
      default: () => ({}),
    },
  },
  computed: {
    ...mapGetters({
      country: 'project/getCountry',
      getCountrySubLevelNames: 'countries/getCountrySubLevelNames',
      getCountryFirstSubLevel: 'countries/getCountryFirstSubLevel',
      getCountrySecondSubLevel: 'countries/getCountrySecondSubLevel',
    }),
    countrySubLevelNames() {
      return this.getCountrySubLevelNames(this.country)
    },
    countryFirstSubLevel() {
      const result = this.getCountryFirstSubLevel(this.country)
      return result || []
    },
    countrySecondSubLevel() {
      const result = this.getCountrySecondSubLevel(this.country)
      return result || []
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.SubNationalCoverageField {
  width: 100%;

  .SimpleField {
    &.FirstSubLevel {
    }
  }
}
</style>
