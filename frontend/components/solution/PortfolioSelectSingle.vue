<template>
  <lazy-el-select
    v-model="innerValue"
    :multiple="multiple"
    :disabled="disabled"
    :placeholder="$gettext('Innovation Portfolios') | translate"
    filterable
    popper-class="PortfolioSelectorPopper"
    class="CountrySelector"
  >
    <el-option v-for="portfolio in portfolios" :key="portfolio.id" :label="portfolio.name" :value="portfolio.id" />
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
  },
  computed: {
    ...mapGetters({
      portfolios: 'portfolio/getPortfolios',
    }),
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

.PortfolioSelectorPopper {
  max-width: @advancedSearchWidth - 40px;
}
</style>
