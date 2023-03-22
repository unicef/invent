<template>
  <lazy-el-select
    v-model="innerValue"
    :multiple="multiple"
    :disabled="disabled"
    :placeholder="$gettext('Innovation Portfolio') | translate"
    filterable
    popper-class="PortfolioSelectorPopper"
    class="CountrySelector"
    ref="portfolioSelectSingle"
  >
    <el-option
      v-for="portfolio in filteredPortfolios"
      :key="portfolio.id"
      :label="portfolio.name"
      :value="portfolio.id"
      :disabled="portfolio.disabled"
    />
  </lazy-el-select>
</template>

<script>
import { mapGetters } from 'vuex'
import VeeValidationMixin from '@/components/mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '@/components/mixins/ProjectFieldsetMixin.js'
export default {
  model: {
    prop: 'value',
    event: 'change',
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  props: {
    value: {
      type: Number,
      default: null,
    },
    portfoliosList: {
      type: Array,
      default: [],
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    publishRules: {},
    draftRules: {},
    apiErrors: {},
  },
  $_veeValidate: {
    value() {
      return this.value
    },
    events: 'change|blur',
    //  rejectsFalse: true,
  },
  computed: {
    ...mapGetters({
      portfolios: 'solution/getPortfoliosList',
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
    filteredPortfolios() {
      if (!this.portfoliosList.length > 0) {
        return this.portfolios
      } else {
        return this.portfolios.map((portfolio) =>
          this.portfoliosList.some((port) => port.portfolio_id === portfolio.id)
            ? { ...portfolio, disabled: true }
            : { ...portfolio, disabled: false }
        )
      }
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
