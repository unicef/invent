<template>
  <div class="ErrorPage">
    <div class="ErrorMessage">
      <div>
        <h2>{{ status }}</h2>
        <p class="StatusText">
          {{ statusText }}
        </p>
        <p class="Details">
          {{ details }}
        </p>
      </div>
      <span><fa icon="code" /></span>
    </div>

    <django-feedback />
  </div>
</template>

<script>
import get from 'lodash/get'
import DjangoFeedback from '@/components/DjangoFeedback.vue'

export default {
  components: {
    DjangoFeedback,
  },
  layout: 'error-layout',
  props: {
    error: {
      type: null,
      default: null,
    },
  },
  computed: {
    response() {
      return get(this, 'error.response', undefined)
    },
    status() {
      return get(this, 'response.status', get(this, 'error.statusCode', 500))
    },
    statusText() {
      return get(
        this,
        'response.statusText',
        get(this, 'error.message', this.$gettext('Server error'))
      )
    },
    details() {
      return get(this, 'response.data.details', null)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.ErrorPage {
  width: 100%;
  height: calc(100vh - @topBarHeightSubpage - @appFooterHeight);
  margin: 0;
  padding: 0;

  .ErrorMessage {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    width: @cardSizeSmall;
    padding: 40px;

    > div {
      position: relative;
      z-index: 20;
    }

    > span {
      position: absolute;
      z-index: 1;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    }
  }

  .svg-inline--fa {
    font-size: @fontSizeHeading * 10;
    color: darken(@colorGrayLighter, 0%);
  }

  h2 {
    margin: 0;
    font-size: @fontSizeHeading * 2;
    color: @colorDanger;
  }

  .StatusText {
    font-size: @fontSizeLarger;
    line-height: 19px;
  }

  .Details {
    margin: 0;
    padding: 0 40px;
    color: @colorTextSecondary;
    font-size: @fontSizeSmall;
    line-height: 16px;
  }
}
</style>
