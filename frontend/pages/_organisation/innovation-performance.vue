<template>
  <div :class="`SectionWrapper ${fullScreen ? 'fullscreen' : ''}`">
    <translate v-if="!fullScreen" tag="h1">Innovation performance</translate>
    <template v-if="true">
      <el-tabs v-model="mainTabs" class="EmbedWrapper">
        <div class="fullscreen-button" @click="fullScreen = !fullScreen">
          <fa v-if="fullScreen" icon="compress" />
          <fa v-else icon="expand" />
        </div>

        <el-tab-pane :label="globalPerformance" name="global" :class="`EmbedContent ${fullScreen ? 'fullscreen' : ''}`">
          <iframe seamless :src="globalPerformanceUrl" class="mainIframe" />
        </el-tab-pane>
        <el-tab-pane
          :label="innovationPortfoliosTitle"
          name="overview"
          :class="`EmbedContent ${fullScreen ? 'fullscreen' : ''}`"
        >
          <p v-if="innovationPortfoliosIntro">{{ innovationPortfoliosIntro }}</p>
          <p v-if="!showSubTabs" class="warning">
            <i class="el-icon-warning-outline"></i>
            <translate class="warning">Please provide proper URLs for each tab.</translate>
          </p>
          <el-tabs v-model="subTabs" class="SubWrapper">
            <el-tab-pane
              v-for="tab in nestedTabs"
              :key="tab.urlTag"
              :label="tab.title"
              :name="tab.tab"
              :class="`SubContent ${fullScreen ? 'fullscreen' : ''}`"
            >
              <iframe seamless :src="tab.url" />
            </el-tab-pane>
          </el-tabs>
        </el-tab-pane>
      </el-tabs>
    </template>
    <template v-else class="disabled">
      <translate>Please provide proper title (innovation_performance_title) in order to turn on this feature!</translate>
    </template>
  </div>
</template>

<script>
export default {
  data() {
    return {
      globalPerformance: this.$gettext('Global performance'),
      innovationPortfoliosTitle: this.$gettext('Innovation Portfolios'),
      innovationPortfolios: [
        {
          title: this.$gettext('Overview'),
          tab: 'overview',
          urlTag: 'innovation_portfolios_1_overview_url',
          url: this.$gettext('innovation_portfolios_1_overview_url'),
        },
        {
          title: this.$gettext('Climate'),
          tab: 'climate',
          urlTag: 'innovation_portfolios_2_climate_url',
          url: this.$gettext('innovation_portfolios_2_climate_url'),
        },
        {
          title: this.$gettext('Gender'),
          tab: 'gender',
          urlTag: 'innovation_portfolios_3_gender_url',
          url: this.$gettext('innovation_portfolios_3_gender_url'),
        },
        {
          title: this.$gettext('Humanitarian'),
          tab: 'humanitarian',
          urlTag: 'innovation_portfolios_4_humanitarian_url',
          url: this.$gettext('innovation_portfolios_4_humanitarian_url'),
        },
        {
          title: this.$gettext('Immunization'),
          tab: 'immunization',
          urlTag: 'innovation_portfolios_5_immunization_url',
          url: this.$gettext('innovation_portfolios_5_immunization_url'),
        },
        {
          title: this.$gettext('Learning'),
          tab: 'learning',
          urlTag: 'innovation_portfolios_6_learning_url',
          url: this.$gettext('innovation_portfolios_6_learning_url'),
        },
        {
          title: this.$gettext('Health'),
          tab: 'health',
          urlTag: 'innovation_portfolios_7_health_url',
          url: this.$gettext('innovation_portfolios_7_health_url'),
        },
        {
          title: this.$gettext('Mental health'),
          tab: 'mental',
          urlTag: 'innovation_portfolios_8_mental_health_url',
          url: this.$gettext('innovation_portfolios_8_mental_health_url'),
        },
        {
          title: this.$gettext('WASH'),
          tab: 'wash',
          urlTag: 'innovation_portfolios_9_wash_url',
          url: this.$gettext('innovation_portfolios_9_wash_url'),
        },
        {
          title: this.$gettext('Youth'),
          tab: 'youth',
          urlTag: 'innovation_portfolios_10_youth_url',
          url: this.$gettext('innovation_portfolios_10_youth_url'),
        },
      ],
      mainTabs: 'global',
      subTabs: 'overview',
      fullScreen: false,
    }
  },
  computed: {
    innovationPerformanceFeature() {
      const title = this.$gettext('innovation_performance_title')
      return !(title === 'innovation_performance_title' || '')
    },
    globalPerformanceUrl() {
      const url = this.$gettext('global_performance_url')
      return url === 'global_performance_url' || '' ? '' : url
    },
    innovationPortfoliosIntro() {
      const intro = this.$gettext('innovation_portfolios_intro')
      return intro === 'innovation_portfolios_intro' || '' ? '' : intro
    },
    nestedTabs() {
      return this.innovationPortfolios.filter((tab) => {
        const what = tab.url !== tab.urlTag
        return what
      })
    },
    showSubTabs() {
      return this.nestedTabs.length > 0
    },
  },
  mounted() {
    document.getElementsByClassName('footer-bg')[0].remove()
    document.getElementsByClassName('vue-django-feedback')[0].remove()
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';

.SectionWrapper {
  padding-top: 20px;
  background-color: white;
  &.fullscreen {
    position: fixed;
    inset: 0;
    z-index: 20;
    padding-top: 8px;
  }
  h1 {
    color: @colorBrandPrimary;
    font-size: @fontSizeHeading;
    letter-spacing: -1px;
    line-height: 1;
    font-weight: 100;
    padding: 10px 40px;
  }
  .warning {
    color: orange;
    font-size: @fontSizeLarger;
    i {
      width: 48px;
    }
  }
  .EmbedWrapper {
    .el-tabs__header {
      padding: 0 40px;
    }
    .el-tabs__content {
      overflow: initial;
    }
    .el-tabs__item {
      font-size: @fontSizeLarger;
    }
    .SubWrapper {

      .el-tabs__item {
        font-size: @fontSizeBase;
      }
      .SubContent {
        position: relative;
        height: calc(100vh - 437px);
        overflow: hidden;
        &.fullscreen {
          height: calc(100vh - 253px);
        }
        iframe {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-color: transparent;
          border: 0px none transparent;
          padding: 0px;
          overflow: hidden;
        }
      }
    }
    .EmbedContent {
      position: relative;
      height: calc(100vh - 225px);
      overflow: auto;
      &.fullscreen {
        height: calc(100vh - 62px);
      }
      iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: transparent;
        border: 0px none transparent;
        padding: 0px;
        overflow: hidden;
      }
      .disabled {
        display: grid;
        place-items: center;
        height: 100%;
        font-size: @fontSizeHeadline;
      }
      p {
        padding: 0 40px;
      }
    }
  }
  .fullscreen-button {
    position: absolute;
    cursor: pointer;
    top: -50px;
    right: 50px;
    padding: 0;
    font-size: 24px;
    color: @colorBrandPrimary;
    &:focus {
      outline: none;
    }
  }
}
</style>
