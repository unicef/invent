<template>
  <div class="CountryFilters">
    <country-select
      v-model="selectedCounties"
      :disabled="disableCountries"
    />
    <region-select
      v-model="selectedRegion"
      :disabled="disableRegions"
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
      selectedCounties: ['dashboard', 'getFilteredCountries', 'setFilteredCountries'],
      selectedRegion: ['dashboard', 'getFilteredRegion', 'setFilteredRegion']
    }),
    disableCountries () {
      return !!this.selectedRegion || this.dashboardType === 'country';
    },
    disableRegions () {
      return this.selectedCounties.length > 0 || this.dashboardType === 'country';
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
