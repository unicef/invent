<template>
  <div class="WelcomeBox-holder">
    <transition name="el-zoom-in-top">
      <div v-show="showWelcomeBox" class="WelcomeBox">
        <h2><translate>Welcome!</translate></h2>
        <h6>{{ welcomeText }}</h6>

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
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.WelcomeBox-holder {
  .WelcomeBox {
    z-index: 410;
    position: absolute;
    bottom: 40px;
    left: 40px;
    box-sizing: border-box;
    overflow: hidden;
    width: 360px;
    // TODO
    // max-height: ???
    padding: 20px 40px;
    color: @colorWhite;
    background: fade(@colorBrandPrimary, 90%);
    box-shadow: 5px 5px 20px 0 rgba(0, 0, 0, 0.15);

    h2 {
      font-size: 36px;
      font-weight: 100;
      margin: 20px 0;
    }

    h6 {
      font-size: 18px;
      font-weight: 100;
      margin: 10px 0 20px;
      // TODO
      overflow: hidden;
      display: -webkit-box;
      -webkit-line-clamp: 10;
      -webkit-box-orient: vertical;
      //
    }

    .CloseWelcomeBox {
      position: absolute;
      top: 16px;
      right: 16px;
      width: 40px;
      height: 40px;
      background-color: transparent;
      color: white;
    }
  }
}
</style>
