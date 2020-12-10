// utilities
import {
  dataInfoFill,
  fillArr,
  phaseInfo,
  lastLabelType,
} from '@/utilities/charts'
import { formatDate } from '@/utilities/projects'
import { isBefore } from 'date-fns'

export const state = () => ({
  stages: {
    stagesChartdata: {},
    stagesOptions: {},
  },
})

export const actions = {
  getStageData({ commit, rootState }, stages) {
    // phases
    const phases = [''].concat(stages.map((i) => i.name))
    // notes
    const notes = [''].concat(stages.map((i) => i.note))

    // labels
    const start = formatDate(rootState.project.start_date)
    const end = formatDate(rootState.project.end_date)
    const today = formatDate(new Date())

    const labels = [start].concat(
      stages.filter((i) => i.checked).map((i) => formatDate(i.date))
    )
    // const lastLabel = labels[labels.length - 1];

    // data
    const data = [0].concat(
      stages.filter((i) => i.checked).map((i) => phases.indexOf(i.name))
    )
    const lastDataPoint = data[data.length - 1]

    // today and end date data points, if needed
    if ((end && isBefore(today, end)) || end === '1970-01-01') {
      data.push(lastDataPoint + 1)
      labels.push([today, 'Today'])
    }
    if (end && end !== '1970-01-01') {
      data.push(data[data.length - 1])
      labels.push([end, 'Ended'])
      notes.push(rootState.project.end_date_note)
    }

    const lLen = labels.length
    // start calc
    const startData = data.slice(0, 1)
    // end calc
    const endData =
      Array.isArray(labels[lLen - 1]) && labels[lLen - 1][1] === 'Ended'
        ? fillArr(lLen - 1, NaN).concat(data.slice(-1))
        : []
    // today calc
    const checkLabels = labels.filter((i) => Array.isArray(i))
    const todayIncludes = checkLabels.filter((i) => i[1] === 'Today')
    const todayData =
      todayIncludes.length > 0
        ? fillArr(lLen - checkLabels.length - 1, NaN).concat(
            checkLabels.length > 1 ? data.slice(-3, -1) : data.slice(-2)
          )
        : []
    // stages calc
    const stagesData =
      todayIncludes.length > 0 ? data.slice(0, -checkLabels.length) : data

    const { color, rotation, dash, point } = phaseInfo(lastLabelType(labels))

    const datasets = Object.freeze([
      {
        borderColor: '#558B2F',
        pointBackgroundColor: '#558B2F',
        fill: false,
        lineTension: 0,
        pointStyle: dataInfoFill(labels.length - 1, 'circle', 'triangle'),
        pointRadius: dataInfoFill(labels.length - 1, 6, 12),
        pointHoverRadius: dataInfoFill(labels.length - 1, 8, 14),
        pointBorderColor: 'white',
        pointRotation: 90,
        data: startData,
      },
      {
        borderColor: color,
        pointBackgroundColor: color,
        fill: false,
        lineTension: 0,
        borderDash: dash,
        pointStyle: dataInfoFill(labels.length, 'circle', point, 'back'),
        pointRadius: dataInfoFill(labels.length, 0, 12, 'back'),
        pointHoverRadius: dataInfoFill(labels.length, 0, 14, 'back'),
        pointBorderColor: 'white',
        pointRotation: rotation,
        data: endData,
      },
      {
        borderColor: '#008DC9',
        pointBackgroundColor: '#008DC9',
        fill: false,
        lineTension: 0,
        pointStyle: dataInfoFill(labels.length - 1, 'circle', 'circle'),
        pointRadius: dataInfoFill(labels.length - 1, 6, 0),
        pointHoverRadius: dataInfoFill(labels.length - 1, 8, 0),
        pointBorderColor: 'white',
        pointRotation: 90,
        data: stagesData,
      },
      {
        borderColor: '#B9B9B9',
        pointBackgroundColor: 'white',
        fill: false,
        lineTension: 0,
        borderDash: [10, 5],
        pointStyle: dataInfoFill(labels.length, 'circle', 'circle', 'back'),
        pointRadius: dataInfoFill(labels.length, 5, 0, 'back'),
        pointHoverRadius: dataInfoFill(labels.length, 7, 0, 'back'),
        pointBorderColor: '#B9B9B9',
        pointBorderWidth: 2,
        pointRotation: 0,
        data: todayData,
      },
    ])
    const chartdata = { labels, datasets }

    commit('SET_STAGES_CHART_DATA', chartdata)
    commit('SET_STAGES_OPTIONS', {
      maintainAspectRatio: false,
      defaultFontColor: '#474747',
      defaultFontSize: 12,
      tooltips: {
        enabled: true,
        callbacks: {
          label: (tooltipItem, data) => {
            return null
          },
          title: (tooltipItem, data) => {
            const { xLabel, yLabel } = tooltipItem[0]
            if (phases[yLabel] === '') {
              return xLabel
            }
            if (Array.isArray(xLabel)) {
              return [xLabel[0], xLabel[1]]
            }
            return [xLabel, phases[yLabel]]
          },
          footer: (tooltipItem, data) => {
            const { xLabel, yLabel } = tooltipItem[0]
            if (xLabel.includes('Ended')) {
              return `Note: ${notes[notes.length - 1]}`.match(/.{1,38}/g)
            }
            return notes[yLabel]
              ? `Note: ${notes[yLabel]}`.match(/.{1,38}/g)
              : null
          },
        },
        backgroundColor: '#474747',
        xPadding: 12,
        yPadding: 12,
        titleMarginBottom: 0,
        footerMarginTop: 8,
        footerFontStyle: 'normal',
        footerAlign: 'center',
        titleAlign: 'center',
        titleFontSize: 12,
        bodyFontSize: 12,
        bodyAlign: 'center',
        displayColors: false,
      },
      legend: {
        display: false,
      },
      scales: {
        xAxes: [
          {
            offset: true,
            gridLines: {
              display: false,
              drawBorder: false,
            },
            ticks: {
              padding: 12,
              // fontStyle: 'bold'
            },
          },
        ],
        yAxes: [
          {
            gridLines: {
              drawBorder: false,
              // color: axisYColors(phases, labels, data)
            },
            ticks: {
              stepSize: 1,
              min: 0,
              max: stages.length,
              fontColor: '#9E9E9E',
              padding: 12,
              callback(value, index, values) {
                return value > 0 ? `${value}. ${phases[value]}` : phases[value]
              },
            },
          },
        ],
      },
    })
  },
}

export const mutations = {
  SET_STAGES_CHART_DATA: (state, obj) => {
    state.stages.chartdata = obj
  },
  SET_STAGES_OPTIONS: (state, obj) => {
    state.stages.options = obj
  },
}
