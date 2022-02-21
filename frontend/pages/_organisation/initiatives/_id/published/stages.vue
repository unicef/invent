<template>
  <section class="stage-graph">
    <p><translate>initiative phases</translate></p>
    <div>
      <cStages />
    </div>
  </section>
</template>

<script>
import { fetchProjectData } from '@/utilities/projects'
import cStages from '@/components/common/chart/cStages'

export default {
  components: {
    cStages,
  },
  async fetch({ store, params, error }) {
    store.dispatch('landing/resetSearch')
    await fetchProjectData(store, params, error)
    if (!store.state.project.published || store.state.project.published.name === null) {
      error({
        statusCode: 404,
        message: 'Initiative is not published',
      })
    }
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';

.stage-graph {
  width: 1200px;
  margin: 0 auto;
  > p {
    padding: 0;
    margin: 20px;
    color: @colorTextSecondary;
    font-weight: bold;
    font-size: 11px;
    text-align: center;
    text-transform: uppercase;
  }
  > div {
    padding-top: 10px;
    background-color: @colorWhite;
    border: 1px solid @colorGrayLight;
    box-shadow: 0 1px 0 0 @colorGrayLight;
  }
}
</style>
