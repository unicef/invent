<template>
  <div class="footer-bg">
    <img class="logo-who" src="/unicef-logo-footer-blue.png" alt="WHO" loading="lazy" />
    <div class="text">
      <span><translate>Disclaimer:</translate>&nbsp;</span>
      <span>
        <span v-html="translateFooter"> </span>
      </span>
      <nuxt-link :to="localePath({ name: 'organisation-terms', params: $route.params })">
        <translate>Terms of use</translate>
      </nuxt-link>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    translateFooter() {
      return this.$gettext(
        'All reasonable precautions have been taken by the UNICEF to verify the information contained in this publication. However, the published material is being distributed without warranty of any kind, either expressed or implied. The responsibility for the interpretation and use of the material lies with the reader. In no event shall the UNICEF be liable for damages arising from its use. Please read our'
      )
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.footer-bg {
  display: flex;
  align-items: center;
  justify-content: center;
  height: @appFooterHeight;
  background-color: #a8a8a9;

  .logo-who {
    width: 79px;
    margin-top: -16px;
    margin-right: 26px;
    z-index: 10;
  }

  .text {
    max-width: 1185px;
    font-size: @fontSizeSmall - 1;
    line-height: 18px;
    color: @colorWhite;

    @media only screen and (max-width: 1360px) {
      font-size: @fontSizeSmall - 2;
      line-height: 15px;
    }
  }

  a {
    color: inherit;
    margin: 0 4px;
  }
}
</style>
