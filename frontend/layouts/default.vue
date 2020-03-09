<template>
  <div :class="layoutClass">
    <dialogs-container />
    <top-bar />
    <action-bar v-if="showActionBar" />
    <nuxt />
    <dha-footer />
    <django-feedback />
  </div>
</template>

<script>
import HeadMixin from '@/layouts/HeadMixin';
import DhaFooter from '../components/common/DhaFooter.vue';
import TopBar from '../components/common/TopBar.vue';
import ActionBar from '../components/common/ActionBar.vue';
import DialogsContainer from '../components/dialogs/DialogsContainer.vue';
import DjangoFeedback from '../components/DjangoFeedback.vue';

export default {
  components: {
    DhaFooter,
    TopBar,
    ActionBar,
    DialogsContainer,
    DjangoFeedback
  },
  mixins: [HeadMixin],
  computed: {
    pureRoute () {
      if (this.$route && this.$route.name) {
        return this.$route.name.split('___')[0];
      }
      return null;
    },
    showActionBar () {
      const hiddenOn = ['index-login', 'index-signup'];
      if (this.$route && this.$route.name) {
        return !hiddenOn.includes(this.pureRoute);
      }
      return false;
    },
    layoutClass () {
      if (!['organisation', 'organisation-login', 'organisation-signup', 'organisation-reset-key'].includes(this.pureRoute)) {
        return 'SubPage';
      } else if (this.$route.params.organisation !== '-') {
        return 'CountryDonorLandingPage';
      }
      return 'LandingPage';
    }
  }

};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .LandingPage {}

  .CountryDonorLandingPage {
    .TopBar {
      .TopBarInner {
        height: @topBarHeightSubpage;

        .LogoHolder {
          .LogoWHO,
          .Separator {
            display: none;
          }
        }
      }
    }
  }

  .SubPage {
    .TopBar {
      .TopBarInner {
        height: @topBarHeightSubpage;

        .LogoHolder {
          .LogoWHO,
          .Separator {
            display: none;
          }
        }
      }
    }
  }
</style>
