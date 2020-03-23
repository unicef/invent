<template>
  <div class="CountryFilters">
    <region-select
      v-model="selectedRegion"
      :disabled="disabledRegions"
    />
    <country-select
      v-model="selectedCountries"
      :disabled="disabledCountries"
    />
    <country-office-select
      v-model="selectedCountryOffice"
      :disabled="disabledCountryOffice"
      :regionFilter="selectedRegion"
    />
  </div>
</template>

<script>
import { mapGettersActions } from '../../utilities/form.js';

import CountrySelect from '../common/CountrySelect';
import CountryOfficeSelect from '@/components/common/CountryOfficeSelect';
import RegionSelect from '../common/RegionSelect';
import FieldOfficeSelector from '../project/FieldOfficeSelector';
import { mapGetters } from 'vuex';
export default {
  components: {
    CountrySelect,
    CountryOfficeSelect,
    RegionSelect,
    FieldOfficeSelector
  },
  computed: {
    ...mapGetters({
      dashboardType: 'dashboard/getDashboardType'
    }),
    ...mapGettersActions({
      selectedCountries: ['dashboard', 'getFilteredCountries', 'setFilteredCountries'],
      selectedRegion: ['dashboard', 'getFilteredRegion', 'setFilteredRegion'],
      selectedCountryOffice: ['dashboard', 'getFilteredCountryOffice', 'setFilteredCountryOffice']
    }),
    disabledCountries () {
      return typeof(this.selectedRegion) === 'number' ? true : false;
    },
    disabledCountryOffice () {
      return typeof(this.selectedRegion) === 'number' ? false : true;
    },
    disabledRegions () {
      return this.selectedCountries.length > 0 ? true : false;
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
      this.selectedCountryOffice = null;
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
