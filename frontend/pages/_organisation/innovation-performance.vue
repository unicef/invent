<template>
  <div class="SectionWrapper">
    <h1><translate>Innovation performance</translate></h1>
    <!--
      Currently always turned on, even though the navigation is hidden .
      Need to check with 'innovationPerformanceFeature' before release
    -->
    <template v-if="true">
      <el-tabs v-model="activeName" class="EmbedWrapper" @tab-click="handleClick">
        <el-tab-pane :label="globalPerformance" name="global" class="EmbedContent">
          <iframe seamless :src="globalPerformanceUrl" />
        </el-tab-pane>
        <el-tab-pane :label="portfolioOverview" name="overview" class="EmbedContent">
          <iframe seamless :src="portfolioOverviewUrl" />
        </el-tab-pane>
        <el-tab-pane :label="portfolioDetails" name="details" class="EmbedContent">
          <iframe seamless :src="portfolioDetailsUrl" />
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
      portfolioOverview: this.$gettext('Portfolio overview'),
      portfolioDetails: this.$gettext('Portfolio details'),
      activeName: 'global',
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
    portfolioOverviewUrl() {
      const url = this.$gettext('portfolio_overview_url')
      return url === 'portfolio_overview_url' || '' ? '' : url
    },
    portfolioDetailsUrl() {
      const url = this.$gettext('portfolio_details_url')
      return url === 'portfolio_details_url' || '' ? '' : url
    },
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event)
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';

.SectionWrapper {
  padding-top: 20px;
  background-color: white;
  h1 {
    color: @colorBrandPrimary;
    font-size: @fontSizeTitle;
    letter-spacing: -1px;
    line-height: 1;
    font-weight: 100;
    padding: 0 40px;
  }
  .EmbedWrapper {
    ::v-deep .el-tabs__header {
      padding: 0 40px;
    }
    .EmbedContent {
      position: relative;
      height: calc(100vh - 250px);
      overflow: hidden;
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
    }
  }
}
</style>
