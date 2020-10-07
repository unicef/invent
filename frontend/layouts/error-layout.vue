<template>
  <div class="SubPage">
    <dialogs-container />
    <top-bar error-page />
    <nuxt />
    <dha-footer />
    <django-feedback />
  </div>
</template>

<script>
import HeadMixin from '@/layouts/HeadMixin'
import DhaFooter from '../components/common/DhaFooter.vue'
import TopBar from '../components/common/TopBar.vue'
import DialogsContainer from '../components/dialogs/DialogsContainer.vue'
import DjangoFeedback from '../components/DjangoFeedback.vue'

export default {
  components: {
    DhaFooter,
    TopBar,
    DialogsContainer,
    DjangoFeedback,
  },
  mixins: [HeadMixin],
  computed: {
    layoutClass() {
      if (this.$route.params.organisation !== '-') {
        return 'CountryDonorLandingPage'
      }
      return 'SubPage'
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.LandingPage {
}

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
