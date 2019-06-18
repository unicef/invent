<template>
  <lazy-el-select
    v-model="innerValue"
    :multiple="multiple"
    :disabled="disabled"
    :placeholder="$gettext('Select country') | translate"
    filterable
    popper-class="CountrySelectorPopper"
    class="CountrySelector"
  >
    <el-option
      v-for="country in countries"
      :key="country.id"
      :label="country.name"
      :value="country.id"
    />
  </lazy-el-select>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  model: {
    prop: 'value',
    event: 'change'
  },
  props: {
    value: {
      type: [Number, Array],
      default: null
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapGetters({
      countries: 'countries/getCountries'
    }),
    innerValue: {
      get () {
        return this.value;
      },
      set (value) {
        this.$emit('change', value);
      }
    },
    multiple () {
      return Array.isArray(this.value);
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .CountrySelectorPopper {
    max-width: @advancedSearchWidth - 40px;
  }
</style>
