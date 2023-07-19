<template>
  <div class="flag-info">
    <el-col class="CountryHolder">
      <el-row type="flex">
        <el-col>
          <div class="country-text">
            <div class="CountryName">
              {{ landingData.name }}
              <span><img :src="countryFlag" alt="country flag" class="CountryFlag" loading="lazy" /></span>
            </div>
            <p>
              <translate>
                Welcome to country view. This view is scoped to show all initiatives of the chosen country.
              </translate>
            </p>
            <nuxt-link
              data-test="country-inventory-link"
              :to="
                localePath({
                  name: 'organisation-inventory-list',
                  params: this.landingData.code,
                  query: { ...this.$route.query, country: this.landingData.id },
                })
              "
            >
              <translate>See this country's initiatives in the inventory</translate>
            </nuxt-link>
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

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.flag-info {
  height: 100px;
  width: inherit;
  margin: 12px auto;
  padding: 8px 36px 8px @leftHomepageIndentation;
  display: flex;

  justify-content: start;

  .CountryHolder {
    display: flex;
    align-items: center;
    width: fit-content;

    .CountryFlag {
      position: relative;
      top: 2px;
      height: 22px;
      margin-left: 6px;
    }
    .country-text {
      display: flex;
      height: 100%;
      flex-direction: column;

      a {
        color: @colorBrandPrimary;
        line-height: 6px;
        padding-bottom: 12px;
      }

      .CountryName {
        margin-top: auto;

        font-size: @fontSizeLarge;
        font-weight: 700;
        color: @colorTextPrimary;
      }
    }
  }
}
</style>
