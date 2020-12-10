import Vue from 'vue'
import { Line } from 'vue-chartjs'

// Vue.component('bar-chart', {
//   extends: Bar,
//   props: ['data', 'options'],
//   mounted () {
//     this.renderChart(this.data, this.options);
//   }
// });

Vue.component('LineChart', {
  extends: Line,
  props: {
    chartdata: {
      type: Object,
      default: null,
    },
    options: {
      type: Object,
      default: null,
    },
  },
  mounted() {
    this.renderChart(this.chartdata, this.options)
  },
})
