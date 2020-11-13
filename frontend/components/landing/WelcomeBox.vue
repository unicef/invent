<template>
  <div class="WelcomeBox-holder">
    <transition name="el-zoom-in-top">
      <div v-show="showWelcomeBox" class="WelcomeBox">
        <h2><translate>Welcome!</translate></h2>
        <!-- TODO: see if is best it should come from backend -->
        <!-- <h6>{{ welcomeText }}</h6> -->
        <h6>
          <translate>
            INVENT provides a one-stop-shop to explore, discover, connect and
            contribute to the landscape of Technology for Development (T4D) and
            Innovations across UNICEF, while improving portfolio management and
            decision making at all levels.
          </translate>
        </h6>
        <el-button class="CloseWelcomeBox" @click="closeWelcomeBox">
          <fa icon="times" />
        </el-button>
      </div>
    </transition>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  data() {
    return {
      visible: true,
    }
  },
  computed: {
    ...mapGetters({
      landingPageDefaults: 'system/getLandingPageDefaults',
      activeCountry: 'landing/getActiveCountry',
      landingData: 'landing/getLandingPageData',
    }),
    showWelcomeBox() {
      return this.visible && !this.activeCountry
    },
    welcomeText() {
      return this.landingData
        ? this.landingData.cover_text
        : this.landingPageDefaults.cover_text
    },
  },
  methods: {
    closeWelcomeBox() {
      this.visible = false
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.WelcomeBox-holder {
  .WelcomeBox {
    z-index: 410;
    position: absolute;
    bottom: 40px;
    left: 40px;
    box-sizing: border-box;
    overflow: hidden;
    width: 400px;
    padding: 20px 20px 48px 40px;
    color: @colorWhite;
    background: fade(@colorBrandPrimary, 90%);
    box-shadow: 5px 5px 20px 0 rgba(0, 0, 0, 0.15);

    h2 {
      font-size: 34px;
      font-weight: 100;
      letter-spacing: -1px;
      line-height: 45px;
      margin: 10px 0 24px;
    }

    h6 {
      font-size: 16px;
      font-weight: 100;
      margin: 0;
      overflow: hidden;
      letter-spacing: -0.25px;
      line-height: 27px;
      display: -webkit-box;
      -webkit-line-clamp: 10;
      -webkit-box-orient: vertical;
    }

    .CloseWelcomeBox {
      position: absolute;
      padding: 0;
      top: 20px;
      right: 20px;
      width: 12px;
      height: 12px;
      background-color: transparent;
      color: white;
    }
  }
}
</style>
