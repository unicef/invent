<template>
  <div class="flag-info">
    <el-col class="CountryHolder">
      <el-row type="flex">
        <el-col class="CountryHolder">
          <div class="Separator" />
        </el-col>
        <el-col class="CountryHolder">
          <img :src="countryFlag" alt="country flag" class="CountryFlag" loading="lazy" />
        </el-col>
        <el-col>
          <div class="country-text">
            <div class="CountryName">{{ landingData.name }}</div>
            <p>
              <translate>
                Welcome to country view. This view is scoped to show all initiatives of the chosen country.
              </translate>
            </p>
          </div>
        </el-col>
      </el-row>
    </el-col>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters({
      landingData: 'landing/getLandingPageData',
    }),
    countryFlag() {
      if (this.landingData) {
        return `/static/flags/${this.landingData.code.toLowerCase()}.png`
      }
      return null
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.flag-info {
  height: 100px;
  width: inherit;
  margin: 12px;
  padding: 8px 36px 8px 220px;
  display: flex;
  align-items: start;

  .CountryHolder {
    display: flex;
    align-items: center;
    width: fit-content;

    .CountryFlag {
      height: 84px;
      margin-right: 6px;
      padding: 5px 0;
    }
    .country-text {
      display: flex;
      height: 100%;
      flex-direction: column;
      padding-left: 24px;

      .CountryName {
        margin-top: auto;
        font-size: @fontSizeLarge;
        font-weight: 700;
        color: @colorTextPrimary;
        line-height: 24px;
      }
    }
  }
}
</style>
