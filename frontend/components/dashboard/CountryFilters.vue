<template>
  <div class="CountryFilters">
    <region-select
      v-model="selectedRegion"
      :disabled="disableRegions"
    />
    <country-select
      v-model="selectedCountries"
      :disabled="disableCountries"
    />
  </div>
</template>

<script>
import { mapGettersActions } from '../../utilities/form.js';

import CountrySelect from '../common/CountrySelect';
import RegionSelect from '../common/RegionSelect';
import { mapGetters } from 'vuex';
export default {
  components: {
    CountrySelect,
    RegionSelect
  },
  computed: {
    ...mapGetters({
      dashboardType: 'dashboard/getDashboardType'
    }),
    ...mapGettersActions({
      selectedCountries: ['dashboard', 'getFilteredCountries', 'setFilteredCountries'],
      selectedRegion: ['dashboard', 'getFilteredRegion', 'setFilteredRegion']
    }),
    disableCountries () {
      return (!this.selectedRegion && this.selectedRegion !== 0) || this.dashboardType === 'country';
    },
    disableRegions () {
      return this.dashboardType === 'country';
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .CountryFilters {
    .el-select {
      width: 100%;

      &:first-child {
        margin-bottom: 10px;
      }
    }
  }
</style>
