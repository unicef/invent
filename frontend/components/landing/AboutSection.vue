<template>
  <div class="AboutSection">
    <div class="about">
      <translate>About INVENT</translate>
    </div>
    <div class="decription">
      {{ permanentFooterText }}
    </div>
    <div class="partners">
      <div v-for="partner in partners" :key="partner.name">
        <img :src="partner.logo" :alt="partner.name" loading="lazy" />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  data() {
    return {
      partners: [
        {
          name: 'WHO',
          logo: '/static/partners/logo-who.png',
        },
        {
          name: 'HRP',
          logo: 'static/partners/logo-hrp-new-cropped.png',
        },
        {
          name: 'UNICEF',
          logo: '/static/partners/unicef-logo-vertical.png',
        },
        {
          name: 'Digital Square',
          logo: '/static/partners/logo-digital_square.png',
        },
        {
          name: 'UNFPA',
          logo: '/static/partners/logo-unfpa.png',
        },
        {
          name: 'PATH',
          logo: '/static/partners/logo-path_new-color.png',
        },
      ],
    }
  },
  computed: {
    ...mapGetters({
      landingData: 'landing/getLandingPageData',
      landingPageDefaults: 'system/getLandingPageDefaults',
    }),
    countrySpecific() {
      return this.landingData !== null
    },
    title() {
      return this.countrySpecific ? this.landingData.footer_title : this.landingPageDefaults.footer_title
    },
    permanentFooterText() {
      return this.landingPageDefaults.permanent_footer
    },
    countryText() {
      if (this.countrySpecific) {
        return this.landingData.footer_text
      }
      return null
    },
    partnerLogos() {
      if (this.countrySpecific) {
        return this.landingData.partner_logos.length > 0 ? this.landingData.partner_logos : null
      }
      return null
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.AboutSection {
  // .limitPageWidth();
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: @colorWhite;
  max-width: 1240px;
  margin: 72px auto;
  margin-bottom: 0px;

  .about {
    text-align: center;
    color: @colorTextPrimary;
    font-size: @fontSizeTitle;
    margin: 46px 0 34px 0;
  }

  .decription {
    text-align: center;
    color: @colorTextPrimary;
    font-size: @fontSizeMedium;
    margin-bottom: 32px;
    width: 1068px;
  }

  .partners {
    display: flex;
    flex-wrap: wrap;
    margin: 18px 24px;
    width: 610px;
    height: 180px;
    margin-bottom: 60px;
    div {
      flex-basis: 33.3333333%;
      display: flex;
      align-items: center;
      justify-content: center;
      img {
        height: 44px;
      }
    }
  }
}
</style>
