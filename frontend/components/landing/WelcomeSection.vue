<template>
  <div class="WelcomeSection">
    <div class="content">
      <h1><translate>Welcome</translate> {{ user.name }}</h1>
      <p>
        <strong>
          <translate> INVENT provides a one-stop-shop to explore, discover, connect and contribute </translate>
        </strong>
        <translate>
          to the landscape of Technology for Development (T4D) and Innovations across UNICEF, while improving portfolio
          management and decision making at all levels.
        </translate>
      </p>
    </div>
    <div class="cta-wrapper">
      <a :href="url">
        <div class="icon">
          <fa icon="book-reader" size="lg" />
        </div>
        <div class="text">
          <translate>Visit INVENT Wiki</translate>
          <fa icon="arrow-right" />
        </div>
      </a>
      <p>
        <translate>
          The Wiki is designed to provide an overview of the less well-known features of the site and to share a vision
          for the direction of the platform.
        </translate>
      </p>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters({
      user: 'user/getProfile',
    }),
    url() {
      return this.$gettext('/en/-/terms')
    },
  },
}
</script>

<style lang="less" scoped>
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.WelcomeSection {
  display: flex;
  .content {
    color: @colorWhite;
    background-color: #4fc8f3;
    // width: calc(100% / 3 * 2);
    // width: 795px;
    flex: 1;
    padding: 40px 55px 45px 110px;
    h1 {
      font-size: @fontSizeHeadline;
      font-weight: normal;
    }
    p {
      font-size: @fontSizeLarge;
      line-height: 27px;
    }
  }
  .cta-wrapper {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: @colorWhite;
    // width: calc(100% / 3 * 1);
    width: 554px;
    background-image: linear-gradient(254deg, #4fc8f3 0%, #00aeef 87.1%, #4fc8f3 87.1%, #4fc8f3 100%);
    a {
      display: flex;
      align-items: center;
      height: 48px;
      background-color: white;
      color: #4fc8f3;
      text-decoration: none;
      font-weight: bold;
      border-radius: 6px;
      overflow: hidden;
      box-shadow: 5px 5px 20px 0 rgba(0, 0, 0, 0.12);
      .icon {
        width: 60px;
        background-color: #4fc8f3;
        color: @colorWhite;
        line-height: 48px;
        background-image: linear-gradient(254deg, #fff 0%, #fff 19%, #4fc8f3 22%, #4fc8f3 87.1%, #4fc8f3 100%);
        svg {
          margin-left: 14px;
        }
      }
      .text {
        padding-left: 13px;
        padding-right: 20px;
        svg {
          margin-left: 8px;
        }
      }
    }
    p {
      margin: 28px 0 0 0;
      text-align: center;
      line-height: 20px;
      font-size: @fontSizeBase;
      max-width: 264px;
    }
  }
}
</style>
