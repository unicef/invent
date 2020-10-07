import merge from 'lodash/merge'
import cloneDeep from 'lodash/cloneDeep'
import forEach from 'lodash/forEach'

import { loadScorecardImages } from '../../webpackRequires'

class ScorecardController {
  constructor($scope, $state, $ngRedux) {
    this.scope = $scope
    this.state = $state
    this.$onInit = this.onInit.bind(this)
    this.$onDestroy = this.onDestroy.bind(this)
    this.createAxisData = this.createAxisData.bind(this)
  }

  importIconTemplates() {
    // Import the whole folder in an collection of string templates, needed for proper webpack optimizations
    const templates = {}
    const templateRequire = loadScorecardImages()
    templateRequire.keys().forEach((item) => {
      const key = item.split('.')[1].replace('/', '')
      templates[key] = templateRequire(item)
    })
    return templates
  }

  onInit() {
    this.dataLoaded = false
    this.structure = window.$nuxt.$store.getters['toolkit/getStructure']
    this.rawData = window.$nuxt.$store.getters['toolkit/getToolkitData']
    this.axesSize = this.rawData.length
    this.images = this.importIconTemplates()
    this.projectId = this.state.params.appName
    this.axisId = this.state.params.axisId
    window.$nuxt.$root.$on('angularjs:mapsAxisChange', this.goToAxis.bind(this))
    this.createAxisData(this.rawData)
  }

  onDestroy() {
    window.$nuxt.$root.$off('angularjs:mapsAxisChange')
  }

  createAxisData(rawData) {
    if (rawData && rawData.length > 0) {
      const data = merge(rawData, this.structure).map((a, key) => {
        const axis = cloneDeep(a)
        axis.id = key
        axis.axisName = axis.axis.split('.')[1]
        axis.axisClass = axis.axis.split('.')[0].replace(' ', '').toLowerCase()
        axis.axisPicture = this.images['icon-' + axis.axisClass]
        forEach(axis.domains, (domain, index) => {
          domain.index = index
        })
        return axis
      })
      this.dataLoaded = true
      this.data = this.summary ? data : data[this.axisId]
    }
    return []
  }

  updateScore(domain, axis) {
    const domainId = domain.index
    const axisId = axis ? axis.id : this.axisId
    this.state.go(this.viewMode ? 'public-maps' : 'mapsToolkit', {
      axisId,
      domainId,
    })
  }

  goToAxis(id) {
    const axisId = id === undefined || id === null ? this.axisId : id

    this.state.go('mapsToolkit', { axisId })
  }

  goToNextAxis() {
    const axisId = parseInt(this.axisId, 10) + 1
    this.state.go('mapsToolkit', { axisId })
  }

  goToSummary() {
    this.state.go('summary')
  }

  goToDashboard() {
    this.state.go('dashboard')
  }

  isLastAxis() {
    return parseInt(this.axisId, 10) + 1 >= this.axesSize
  }

  static scorecardFactory() {
    const scorecard = ($scope, $state, $ngRedux) => {
      require('./Scorecard.scss')
      return new ScorecardController($scope, $state, $ngRedux)
    }
    scorecard.$inject = ['$scope', '$state', '$ngRedux']
    return scorecard
  }
}

export default ScorecardController
