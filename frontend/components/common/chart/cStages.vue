<template>
  <section>
    <line-chart
      v-if="loaded"
      :chartdata="chartdata"
      :options="options"
      class="graph__line"
    />
    <section class="graph__legend">
      <ul class="legend">
        <li><translate>Legend:</translate></li>
        <li>
          <div class="legend__triangle-right" />
          <translate>Project start date</translate>
        </li>
        <li>
          <div class="legend__triangle-down" />
          <translate>Project end date</translate>
        </li>
        <li>
          <div class="legend__cirle legend__circle--blue" />
          <translate>Phase completion date</translate>
        </li>
        <li>
          <div class="legend__cirle legend__circle--grey" />
          <translate>Next phase (incomplete)</translate>
        </li>
        <li>
          <div class="legend__line legend__line--blue" />
          <translate>Completion period</translate>
        </li>
        <li>
          <div class="legend__line legend__line--dashed" />
          <translate>Current period</translate>
        </li>
      </ul>
      <p>
        <translate>
          The date under a phase represents when that phase was completed.
        </translate>
      </p>
    </section>
  </section>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  data: () => ({
    loaded: false,
  }),
  computed: {
    ...mapState({
      chartdata: (state) => state.charts.stages.chartdata,
      options: (state) => state.charts.stages.options,
      stagesDraft: (state) => state.project.stagesDraft,
    }),
  },
  async mounted() {
    await this.loadStagesDraft()
    this.getStageData(this.stagesDraft)
    await setTimeout(() => {
      this.loaded = true
    }, 250)
  },
  beforeDestroy() {
    this.loaded = false
  },
  methods: {
    ...mapActions({
      getStageData: 'charts/getStageData',
      loadStagesDraft: 'project/loadStagesDraft',
    }),
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.graph__line {
  padding: 50px 20px 40px;
}
.graph__legend {
  background-color: #f8f8f8;
  color: #9e9e9e;
  text-align: center;
  font-size: 11px;
  padding: 22px 33px;
  p {
    margin: 0;
  }
}
.legend {
  margin: 0 0 12px;
  li {
    display: inline-block;
    padding: 0 10px;
  }
}
.legend__cirle {
  display: inline-block;
  margin-right: 8px;
  margin-bottom: -1px;
  width: 10px;
  height: 10px;
  border-radius: 10px;
}
.legend__line {
  display: inline-block;
  margin-right: 8px;
  margin-bottom: 3px;
  width: 15px;
  border-top: 2px solid @colorTextMuted;
}
.legend__line--blue {
  border-top-color: @colorBrandPrimary;
}
.legend__line--dashed {
  border-top: 2px dashed @colorTextMuted;
}
.legend__circle--blue {
  background-color: @colorBrandPrimary;
}
.legend__circle--grey {
  width: 6px;
  height: 6px;
  background-color: @colorWhite;
  border: 2px solid @colorTextMuted;
}
.legend__triangle-down {
  display: inline-block;
  margin-right: 8px;
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 8px solid #d86422;
}
.legend__triangle-right {
  display: inline-block;
  margin-right: 8px;
  width: 0;
  height: 0;
  border-top: 5px solid transparent;
  border-left: 9px solid #76bf41;
  border-bottom: 5px solid transparent;
}
</style>
