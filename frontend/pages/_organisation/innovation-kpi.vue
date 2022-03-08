<template>
  <div class="SectionWrapper">
    <div class="StoryWrapper">
      <iframe v-if="innovationPerformanceUrl && innovationPerformanceFeature" :src="innovationPerformanceUrl" />
      <div v-if="!innovationPerformanceFeature" class="disabled">
        <translate>Innovation Performance is disabled</translate>
      </div>
      <div v-if="innovationPerformanceFeature && !innovationPerformanceUrl" class="disabled">
        <translate>Please provide proper content URL!</translate>
      </div>
    </div>
  </div>
</template>

innovationPerformanceFeature

<script>
export default {
  computed: {
    innovationPerformanceFeature() {
      const title = this.$gettext('innovation_performace_title')
      return !(title === 'innovation_performace_title' || '')
    },
    innovationPerformanceUrl() {
      const url = this.$gettext('innovation_performance_url')
      return url === 'innovation_performance_url' || '' ? '' : url
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';

.SectionWrapper {
  padding: 20px 40px 0 40px;
  .StoryWrapper {
    position: relative;
    height: calc(100vh - 140px);
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
</style>
