<template>
  <lazy-el-select
    v-model="innerValue"
    :multiple="false"
    :disabled="disabled"
    :placeholder="$gettext('Country') | translate"
    filterable
    popper-class="CountrySelectorPopper"
    class="CountrySelector"
  >
    <el-option
      v-for="country in filteredCountries"
      :key="country.id"
      :label="country.name"
      :value="country.id"
      :disabled="country.disabled"
    />
  </lazy-el-select>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: Number,
      default: null,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    selectedCountries: {
      type: Array,
      default: null,
    },
  },
  computed: {
    ...mapGetters({
      countries: 'countries/getCountries',
      countriesByRegion: 'countries/getCountriesByUnicefRegion',
    }),
    filteredCountries() {
      if (this.selectedCountries === null) {
        return this.countries.map((country) => ({ ...country, disabled: false }))
      }
      return this.countries.map((country) =>
        this.selectedCountries.some((selCountry) => selCountry.country === country.id)
          ? { ...country, disabled: true }
          : { ...country, disabled: false }
      )
    },
    innerValue: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('change', value)
      },
    },
    multiple() {
      return Array.isArray(this.value)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.CountrySelectorPopper {
  max-width: @advancedSearchWidth - 40px;
}
</style>
