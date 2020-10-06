import forOwn from 'lodash/forOwn'
import { fixUrl } from '../Utilities'

class AssessmentModuleController {
  constructor($scope, $state, $timeout, $ngRedux) {
    this.scope = $scope
    this.state = $state
    this.timeout = $timeout
    this.$ngRedux = $ngRedux
    this.EE = window.EE
    this.$onInit = this.onInit
    this.$onDestroy = this.onDestroy
    this.watchers = this.watchers.bind(this)
    this.fixUrl = fixUrl
  }

  watchers() {
    this.scope.$watch(
      (s) => s.vm.projectData,
      (data) => {
        this.adjustProjectData(data)
      }
    )
    this.scope.$watch(
      (s) => s.vm.coverageVersion,
      (data) => {
        this.adjustCoverageVersions(data)
      }
    )
  }

  onInit() {
    this.isPublic = false
    this.profile = window.$nuxt.$store.getters['user/getProfile']
    this.project = window.$nuxt.$store.getters['projects/getCurrentProject']
    this.projectData = this.project.isPublished
      ? this.project.published
      : this.project.draft
    this.structure = window.$nuxt.$store.getters['projects/getStructure']
    this.toolkitVersion =
      window.$nuxt.$store.getters['projects/getToolkitVersions']
    this.coverageVersion =
      window.$nuxt.$store.getters['projects/getCoverageVersions']
    this.rawToolkitData = window.$nuxt.$store.getters['toolkit/getToolkitData']
    this.mapData = window.$nuxt.$store.getters['countries/getCountryDetails'](
      this.projectData.country
    )
    this.watchers()
    this.projectId = this.state.params.id
    this.resizeEvent()
    this.eventBinding()
  }

  onDestroy() {
    this.eventRemoving()
    this.userType = 0
  }

  resizeEvent() {
    let doit
    this.resizefn = () => {
      clearTimeout(doit)
      doit = setTimeout(this.resizedw, 50)
    }
    window.onresize = this.resizefn
    this.resizedw = () => {
      window.$nuxt.$root.$emit('angularjs:dashResized')
    }
  }

  eventBinding() {
    window.$nuxt.$root.$on(
      'angularjs:mapsDomainChange',
      this.handleChangeDomain.bind(this)
    )
    window.$nuxt.$root.$on(
      'angularjs:mapsAxisChange',
      this.handleChangeAxis.bind(this)
    )
  }

  eventRemoving() {
    window.$nuxt.$root.$off('angularjs:mapsDomainChange')
    window.$nuxt.$root.$off('angularjs:mapsAxisChange')
  }

  adjustProjectData(data) {
    if (this.profile && data && data.country) {
      this.districtProjects = this.parseCoverage(data)
      this.nationalLevelCoverage = data.national_level_deployment
    }
  }

  parseCoverage(data) {
    if (!data || !Array.isArray(data.coverage)) {
      return {}
    }
    const cov = {}
    for (const d of data.coverage) {
      cov[d.district] = {
        clients: d.clients,
        health_workers: d.health_workers,
        facilities: d.facilities,
      }
    }
    return cov
  }

  snapShot() {
    return this.snapShotProject()
  }

  adjustCoverageVersions(data) {
    if (!data || this.isPublic) {
      return
    }

    const coverage = this.projectData.coverage
      ? this.projectData.coverage.slice()
      : []
    coverage.push(Object.assign({}, this.projectData.national_level_deployment))
    data.push({ data: coverage })

    const today = new Date()
    const year = today.getFullYear()
    const month = ('0' + (today.getMonth() + 1)).slice(-2)
    const day = ('0' + today.getDate()).slice(-2)

    const todayString = [year, month, day].join('-')

    const historyChartData = data.reduce(
      (ret, versionObj, vInd) => {
        ret.data[vInd] = {}
        ret.data[vInd].date = versionObj.modified
          ? versionObj.modified.split('T')[0]
          : todayString

        versionObj.data.forEach((distrObj) => {
          forOwn(distrObj, (val, key) => {
            if (key !== 'district') {
              const newKey = key.replace('_', ' ')

              if (!ret.labels.includes(newKey)) {
                ret.labels.push(newKey)
              }

              const name = 'axis' + (ret.labels.indexOf(newKey) + 1)

              ret.data[vInd][name] = (ret.data[vInd][name] || 0) + val
            }
          })
        })

        return ret
      },
      { labels: [], data: [] }
    )
    window.$nuxt.$root.$emit('angularjs:coverageChartData', historyChartData)
  }

  handleChangeDomain(axisId, domainId) {
    if (this.project.isMember || this.project.isViewer) {
      const path = window.$nuxt.$root.localePath({
        name: 'organisation-projects-id-toolkit',
        params: window.$nuxt.$route.params,
        query: { axisId, domainId },
      })
      window.$nuxt.$router.push(path)
    }
  }

  handleChangeAxis(axisId) {
    if (this.project.isMember || this.project.isViewer) {
      const path = window.$nuxt.$root.localePath({
        name: 'organisation-projects-id-toolkit',
        params: window.$nuxt.$route.params,
        query: { axisId, domainId: 0 },
      })
      window.$nuxt.$router.push(path)
    }
  }

  static factory() {
    function assessmentController($scope, $state, $timeout, $ngRedux) {
      require('./Assessment.scss')
      return new AssessmentModuleController($scope, $state, $timeout, $ngRedux)
    }

    assessmentController.$inject = ['$scope', '$state', '$timeout', '$ngRedux']

    return assessmentController
  }
}

export default AssessmentModuleController
