import merge from 'lodash/merge'
import forEach from 'lodash/forEach'
import cloneDeep from 'lodash/cloneDeep'
import map from 'lodash/map'

import { loadHtmlTemplates } from '../webpackRequires'

class MapsToolkitController {
  constructor($scope, $state, $sce) {
    this.state = $state
    this.scope = $scope
    this.$sce = $sce
    this.$onInit = this.onInit.bind(this)
    this.$onDestroy = this.onDestroy.bind(this)
    this.processAxesData = this.processAxesData.bind(this)
  }

  onInit() {
    window.$nuxt.$root.$on(
      'angularjs:mapsAxisChange',
      this.handleChangeAxis.bind(this)
    )
    window.$nuxt.$root.$on(
      'angularjs:mapsDomainChange',
      this.handleChangeDomain.bind(this)
    )
    this.dataLoaded = false
    this.rawData = window.$nuxt.$store.getters['toolkit/getToolkitData']
    this.profile = window.$nuxt.$store.getters['user/getProfile']
    this.viewMode =
      window.$nuxt.$store.getters['projects/getCurrentProject'].isViewer
    this.domainStructure = window.$nuxt.$store.getters[
      'toolkit/getDomainStructure'
    ](this.state.params.axisId, this.state.params.domainId)
    this.score = 0
    this.projectId = this.state.params.appName
    this.domainId = this.state.params.domainId
    this.axisId = this.state.params.axisId
    this.templates = this.importHtmlTemplates()
    this.processAxesData(
      cloneDeep(this.rawData),
      this.state.params.axisId,
      this.state.params.domainId
    )
    this.unsubscribe = window.$nuxt.$store.watch(
      (state, getters) => getters['toolkit/getToolkitData'],
      (toolkitData) => {
        this.scope.$evalAsync(() => {
          this.rawData = toolkitData
          this.processAxesData(
            cloneDeep(this.rawData),
            this.state.params.axisId,
            this.state.params.domainId
          )
        })
      }
    )
  }

  onDestroy() {
    window.$nuxt.$root.$off('angularjs:mapsAxisChange')
    window.$nuxt.$root.$off('angularjs:mapsDomainChange')
    this.unsubscribe()
  }

  handleChangeAxis(axisId) {
    const path = window.$nuxt.$root.localePath({
      name: 'organisation-projects-id-toolkit',
      params: window.$nuxt.$route.params,
      query: { axisId, domainId: 0 },
    })
    window.$nuxt.$router.push(path, () => {
      this.scope.$digest()
    })
  }

  handleChangeDomain(axisId, domainId) {
    const path = window.$nuxt.$root.localePath({
      name: 'organisation-projects-id-toolkit',
      params: window.$nuxt.$route.params,
      query: { axisId, domainId },
    })
    window.$nuxt.$router.push(path, () => {
      this.scope.$digest()
    })
  }

  importHtmlTemplates() {
    // Import the whole folder in an collection of string templates, needed for proper webpack optimizations
    const templates = {}
    const templateRequire = loadHtmlTemplates()
    templateRequire.keys().forEach((item) => {
      const key = item.split('.')[1].replace('/', '')
      templates[key] = templateRequire(item)
    })
    return templates
  }

  processAxesData(data, axisId, domainId) {
    if (data && data.length > 0 && axisId && domainId) {
      this.axis = data[axisId]
      this.domain = data[axisId].domains[domainId]
      this.data = merge(this.domain, this.domainStructure)
      this.score = 0
      forEach(this.data.questions, (question, questionKey) => {
        question.index = questionKey
        question.answers = map(question.answers, (value, index) => {
          let template = null
          if (question.answerTemplate && question.answerTemplate[index]) {
            template = this.$sce.trustAsHtml(
              this.templates[question.answerTemplate[index]]
            )
          }
          this.score += value === -1 ? 0 : value
          return { index, value, template }
        })
      })
      this.dataLoaded = true
    }
  }

  calculateMainBoxSize(question) {
    if (question && question.choices) {
      return 90 - 10 * question.choices.length
    }
    return 40
  }

  checkChecked(questionId, answerId, points) {
    const answer = this.data.questions[questionId].answers[answerId]
    return answer.value === points
  }

  setAnswer(questionId, answerId, points) {
    if (this.viewMode) {
      return
    }
    const answer = {
      axis: this.axisId,
      domain: this.domainId,
      question: questionId,
      answer: answerId,
      value: points,
    }
    window.$nuxt.$store.dispatch('toolkit/saveAnswer', answer)
  }

  printAnswer(answer) {
    if (answer !== null && answer.value === -1) {
      return 0
    }
    return answer.value
  }

  backButtonDisabled() {
    return parseInt(this.domainId, 10) === 0 && parseInt(this.axisId, 10) === 0
  }

  isLastDomainInAxis() {
    return (
      parseInt(this.domainId, 10) >=
      this.rawData[this.axisId].domains.length - 1
    )
  }

  goToNextDomain() {
    let nextDomain = parseInt(this.domainId, 10) + 1
    let nextAxis = parseInt(this.axisId, 10)
    if (nextDomain >= this.rawData[this.axisId].domains.length) {
      nextAxis += 1
      nextDomain = 0
    }
    this.handleChangeDomain(nextAxis, nextDomain)
  }

  goToPrevDomain() {
    let prevDomain = parseInt(this.domainId, 10) - 1
    let prevAxis = parseInt(this.axisId, 10)
    if (prevDomain <= 0) {
      prevAxis -= 1
      prevDomain = this.rawData[prevAxis].domains.length - 1
    }

    this.handleChangeDomain(prevAxis, prevDomain)
  }

  goToScorecard() {
    const axisId = this.axisId
    const path = window.$nuxt.$root.localePath({
      name: 'organisation-projects-id-toolkit-scorecard',
      params: window.$nuxt.$route.params,
      query: { axisId },
    })
    window.$nuxt.$router.push(path, () => {
      this.scope.$digest()
    })
  }

  static mapsControllerFactory() {
    function mapsController($scope, $state, $sce) {
      require('./MapsToolkit.scss')
      return new MapsToolkitController($scope, $state, $sce)
    }

    mapsController.$inject = ['$scope', '$state', '$sce']

    return mapsController
  }
}

export default MapsToolkitController
