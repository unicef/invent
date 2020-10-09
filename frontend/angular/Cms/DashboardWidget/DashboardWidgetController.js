import flatMap from 'lodash/flatMap'
import findIndex from 'lodash/findIndex'
import { getters, actions } from '../../store/modules/cms'

class DashboardWidgetController {
  constructor($scope, $ngRedux) {
    this.scope = $scope
    this.$ngRedux = $ngRedux
    this.$onInit = this.onInit.bind(this)
    this.watchers = this.watchers.bind(this)
    this.splitType = this.splitType.bind(this)
  }

  onInit() {
    this.lessons = []
    this.resources = []
    this.experiences = []
    this.watchers()
    this.unsubscribe = this.$ngRedux.connect(this.mapState, actions)(this)
  }

  mapState(state) {
    const domains = window.$nuxt.$store.getters['system/getDomains']
    const currentDomain = domains[Math.floor(Math.random() * domains.length)]
    return {
      axes: getters.getDomainStructureForCms(state),
      all: getters.getCmsData(state),
      domains,
      currentDomain,
    }
  }

  watchers() {
    this.scope.$watchGroup(
      [(s) => s.vm.currentDomain, (s) => s.vm.scores],
      ([domain, scores]) => {
        if (domain && scores && scores.length > 0) {
          this.setDomainVariables(domain, scores)
          this.splitType(this.all)
        }
      }
    )

    this.scope.$watchCollection((s) => s.vm.all, this.splitType)
  }

  splitType(data) {
    if (this.currentDomain && this.currentDomain.id) {
      const id = this.currentDomain.id
      this.resources = data.filter(
        (item) => item.type === 1 && item.domain === id
      )
      this.lessons = data.filter(
        (item) => item.type === 2 && item.domain === id
      )
      this.experiences = data.filter(
        (item) => item.type === 3 && item.domain === id
      )
    }
  }

  setDomainVariables(domain, scores) {
    this.axisColor = `axis-${domain.axis}`
    this.domainIcon = `domain-${domain.id}`
    if (scores) {
      const domainScores = flatMap(scores, (score) => {
        return score.domains
      })
      const selectedDomain = domainScores.find((score) => {
        return score.id === domain.id
      })
      this.domainScore = Math.round(
        (selectedDomain.domain_sum * 100) / selectedDomain.domain_max
      )
    }
  }

  nextDomain() {
    let next =
      findIndex(this.domains, (d) => d.id === this.currentDomain.id) + 1
    if (next > this.domains.length - 1) {
      next = 0
    }
    this.currentDomain = this.domains[next]
  }

  prevDomain() {
    let prev =
      findIndex(this.domains, (d) => d.id === this.currentDomain.id) - 1
    if (prev === -1) {
      prev = this.domains.length - 1
    }
    this.currentDomain = this.domains[prev]
  }

  static factory() {
    require('./DashboardWidget.scss')
    function dashboardWidgetController($scope, $ngRedux) {
      return new DashboardWidgetController($scope, $ngRedux)
    }
    dashboardWidgetController.$inject = ['$scope', '$ngRedux']
    return dashboardWidgetController
  }
}

export default DashboardWidgetController
