<template>
  <div class="CountryFilters">
    <region-select
      v-model="selectedRegion"
      :disabled="disableRegions"
    />
    <country-select
      v-model="selectedCountries"
      :disabled="disableCountries"
      :region="disableCountries ? -1 : selectedRegion"
    />
    <field-office-selector
      v-model="selectedOffice"
      :country="firstSelectedCountry"
    />
  </div>
</template>

<script>
import { mapGettersActions } from '../../utilities/form.js';

import CountrySelect from '../common/CountrySelect';
import RegionSelect from '../common/RegionSelect';
import FieldOfficeSelector from '../project/FieldOfficeSelector';
import { mapGetters } from 'vuex';
export default {
  components: {
    CountrySelect,
    RegionSelect,
    FieldOfficeSelector
  },
  computed: {
    ...mapGetters({
      dashboardType: 'dashboard/getDashboardType'
    }),
    ...mapGettersActions({
      selectedCountries: ['dashboard', 'getFilteredCountries', 'setFilteredCountries'],
      selectedOffice: ['dashboard', 'getFilteredOffice', 'setFilteredOffice'],
      selectedRegion: ['dashboard', 'getFilteredRegion', 'setFilteredRegion']
    }),
    disableCountries () {
      return (!this.selectedRegion && this.selectedRegion !== 0) || this.dashboardType === 'country';
    },
    disableRegions () {
      return this.dashboardType === 'country';
    },
    firstSelectedCountry () {
      return this.selectedCountries && this.selectedCountries.length ? this.selectedCountries[0] : null;
    }
  },
  watch: {
    selectedCountries (newCountries, oldCountries) {
      if (!newCountries || !newCountries.length || (oldCountries && oldCountries.length && oldCountries[0] !== newCountries[0])) {
        this.selectedOffice = null;
      }
    },
    selectedRegion (newRegion) {
      this.selectedCountries = this.selectedCountries.filter(c => c.unicef_region === newRegion.id);
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
      margin-bottom: 10px;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }
</style>
