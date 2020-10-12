<template>
  <el-row v-if="country" type="flex" align="middle" class="CountryItem">
    <country-flag v-show="showFlag" :code="country.code" />
    <el-col class="CountryName">
      {{ country.name }}
    </el-col>
  </el-row>
</template>

<script>
import { mapGetters } from 'vuex'
import CountryFlag from './CountryFlag'

export default {
  components: {
    CountryFlag,
  },
  props: {
    id: {
      type: Number,
      default: null,
    },
    showFlag: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    ...mapGetters({
      getCountryDetails: 'countries/getCountryDetails',
    }),
    country() {
      if (this.id) {
        return this.getCountryDetails(this.id)
      }
      return null
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.CountryItem {
  .CountryFlag {
    width: 24px;
    height: 14px;
    box-shadow: 0 0 1px 1px @colorGrayLighter;
  }

  .CountryName {
    width: auto;
    margin: 0 12px;
    font-size: @fontSizeBase;
    font-weight: 400;
    line-height: 16px;
    color: @colorBrandPrimary;
  }
}
</style>
