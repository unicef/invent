<template>
  <div class="LandingPage">
    <div class="MapBoxContainer">
      <welcome-box />
      <landing-map v-if="!showCoverImage" />
      <country-projects-box />

      <div
        v-if="showCoverImage"
        :style="{backgroundImage: `url(${landingData.cover_url})`}"
        class="CoverImageBg"
      />
    </div>

    <div class="InfoSignupContainer">
      <el-row type="flex">
        <el-col class="InfoBoxWrapper">
          <info-box />
        </el-col>
        <el-col class="CentralBoxWrapper">
          <central-box />
        </el-col>
      </el-row>
    </div>

    <about-section />
  </div>
</template>

<script>

import LandingMap from '../../components/landing/LandingMap.vue';
import WelcomeBox from '../../components/landing/WelcomeBox.vue';
import CountryProjectsBox from '../../components/landing/CountryProjectsBox.vue';
import InfoBox from '../../components/landing/InfoBox.vue';
import CentralBox from '../../components/landing/CentralBox.vue';
import AboutSection from '../../components/landing/AboutSection.vue';
import { mapGetters, mapActions } from 'vuex';

export default {
  components: {
    LandingMap,
    WelcomeBox,
    InfoBox,
    CentralBox,
    AboutSection,
    CountryProjectsBox
  },
  computed: {
    ...mapGetters({
      landingData: 'landing/getLandingPageData',
      profile: 'user/getProfile'
    }),
    showCoverImage () {
      return this.landingData && this.landingData.cover;
    }
  },
  fetch ({ store }) {
    store.dispatch('landing/resetSearch');
  },
  async mounted () {
    if (!process.server && window.location.hash) {
      const codeMatch = window.location.hash.match(/#code=(.*)&session/);
      window.history.replaceState(null, null, ' ');
      if (codeMatch.length > 1) {
        const code = codeMatch[1];
        this.$nextTick(() => {
          this.$nuxt.$loading.start('loginLoader');
        });
        try {
          await this.login({ code });
        } catch (e) {
          this.$nuxt.$loading.finish('loginLoader');
          return;
        }
        try {
          if (this.profile.country) {
            this.setSelectedCountry(this.profile.country);
          }
          if (this.$route.query && this.$route.query.next) {
            const path = this.$route.query.next;
            const query = { ...this.$route.query, next: undefined };
            this.$router.push({ path, query });
          } else {
            this.$router.push(this.localePath({ name: 'organisation-dashboard-list', params: this.$route.params, query: { country: [this.profile.country] } }));
          }
        } catch (e) {
          console.error(e);
        }
        this.$nuxt.$loading.finish('loginLoader');
      }
    }
  },
  methods: {
    ...mapActions({
      login: 'user/doLogin',
      setSelectedCountry: 'dashboard/setSelectedCountry'
    })
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .LandingPage {
    .MapBoxContainer {
      position: relative;
    }

    .CoverImageBg {
      display: block;
      height: @landingMapHeight;
      min-height: @landingMapMinHeight;
      background-color: @colorGrayLight;
      background-size: cover;
      background-position: center center;
      background-repeat: no-repeat;
    }

    .CoverImage {
      width: 100%;
      height: auto;
    }

    .InfoSignupContainer {
      margin: 40px 0;

      > .el-row {
        align-items: stretch;
      }

      .InfoBoxWrapper {
        min-width: 360px;
        max-width: 360px;
        margin-left: 40px;
        margin-right: 30px;
        background-color: @colorWhite;
      }

      .CentralBoxWrapper {
        margin-right: 40px;
        background-color: @colorBrandPrimary;
      }

      .SignupBox {
        padding: 0 40px;
      }

      .SingupComponent {
        min-height: auto !important;
      }
    }

    h2 {
      font-size: @fontSizeHeading;
    }

    h3 {
      font-size: @fontSizeTitle;
    }

    h4 {
      font-size: @fontSizeLarge;
    }

    h6 {
      font-size: @fontSizeMedium;
      line-height: 24px;
      font-weight: 400;
    }
  }
</style>
