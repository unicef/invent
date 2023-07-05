<template>
  <div class="flag-info">
    <el-col class="CountryHolder">
      <el-row :gutter="30" type="flex">
        <el-col :span="4" class="CountryHolder">
          <img :src="countryFlag" alt="country flag" class="CountryFlag" loading="lazy" />
        </el-col>
        <el-col :span="22">
          <div class="country-text">
            <div class="CountryName">{{ landingData.name }}</div>
            <p>
              <translate>
                Welcome to country view. This view is scoped to show all initiatives of the chosen country.
              </translate>
            </p>
          </div>
        </el-col>
        <el-col :span="4" class="InventoryButton">
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
            <translate>{{ this.landingData.name }} Inventory</translate>
          </nuxt-link>
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
  margin: 12px auto;
  padding: 8px 36px 8px 36px;
  display: flex;

  justify-content: center;

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
      padding-left: 12px;

      .CountryName {
        margin-top: auto;
        font-size: @fontSizeLarge;
        font-weight: 700;
        color: @colorTextPrimary;
        line-height: 24px;
      }
    }
  }
  .InventoryButton {
    display: flex;

    flex-direction: column;
    justify-content: end;
    color: @colorBrandPrimary;

    a {
      margin: auto;
      width: 100px;
      background-color: @colorBrandPrimary;
      color: @colorWhite;
      height: 36px;
      padding: 11px 24px 13px 24px;
      font-size: 16px;
      font-weight: bold;
      letter-spacing: 0;
      line-height: 20px;
      text-align: center;
      text-decoration: none;
      border-radius: 4px;
    }
  }
}
</style>
