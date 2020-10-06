import flatMap from 'lodash/flatMap'
import { getters, actions } from '../../store/modules/cms'

class PlanningAndGuidanceController {
  constructor($scope, $state, $ngRedux) {
    this.scope = $scope
    this.state = $state
    this.$onInit = this.onInit.bind(this)
    this.$onDestroy = this.onDestroy.bind(this)
    this.$postLink = this.postLink.bind(this)
    this.applyFilters = this.applyFilters.bind(this)
    this.extractDomainSelection = this.extractDomainSelection.bind(this)
    this.applyLimitOrSearch = this.applyLimitOrSearch.bind(this)
    this.unsubscribe = $ngRedux.connect(this.mapState, actions)(this)
  }

  onInit() {
    this.createFilters()
    this.lessons = []
    this.resources = []
    this.experiences = []
    this.showLimit = 10
    this.showAllFlag = false
    this.searchText = null
    this.watchers()
  }

  onDestroy() {
    this.unsubscribe()
  }

  mapState(state) {
    return {
      axes: getters.getDomainStructureForCms(state),
      all: getters.getCmsData(state),
    }
  }

  postLink() {
    this.checkHash()
  }

  checkHash() {
    setTimeout(() => {
      const hash = window.location.hash
      if (
        !hash ||
        !['#all', '#lessons', '#experiences', '#resources'].includes(hash)
      ) {
        this.activate('all')
      } else {
        this.activate()
      }
    }, 100)
  }

  toggleShowAll() {
    this.showAllFlag = !this.showAllFlag
  }

  watchers() {
    this.scope.$watch(this.extractDomainSelection, this.applyFilters, true)
    this.scope.$watchGroup(
      [(s) => s.vm.toShow, (s) => s.vm.showAllFlag, (s) => s.vm.searchText],
      this.applyLimitOrSearch
    )
    this.scope.$watchCollection(
      (s) => s.vm.all,
      (data, oldData) => {
        const goTo =
          data.length - oldData.length === 1 ? data.slice(-1)[0].type : null
        this.resources = data.filter((item) => item.type === 1)
        this.lessons = data.filter((item) => item.type === 2)
        this.experiences = data.filter((item) => item.type === 3)
        this.activate(goTo)
      }
    )
  }

  stripHtml(text) {
    const regex = /(<([^>]+)>)/gi
    return text.replace(regex, '')
  }

  applyLimitOrSearch([toShow, showAllFlag, searchText]) {
    if (toShow && showAllFlag) {
      this.showLimit = toShow.length
    } else {
      this.showLimit = 10
    }
    if (searchText && searchText !== this.prevSearchText) {
      this.prevSearchText = searchText
      const slice = this.toShow.slice()
      searchText = searchText.replace(/[-\\^$*+?.()|[\]{}]/g, '\\$&')
      const regex = new RegExp(searchText, 'ig')
      slice.forEach((item) => {
        const strip = this.stripHtml(item.body)
        const name = item.name
        const match = name.match(regex) || strip.match(regex)
        item.searchOccurrences = match ? match.length : 0
      })
      this.scope.$evalAsync(() => {
        this.toShow = slice
      })
    } else if (
      this.toShow &&
      !searchText &&
      searchText !== this.prevSearchText
    ) {
      this.prevSearchText = searchText
      const slice = this.toShow.slice()
      slice.forEach((item) => {
        item.searchOccurrences = 0
      })
      this.scope.$evalAsync(() => {
        this.toShow = slice
      })
    }
  }

  extractDomainSelection() {
    return flatMap(this.filters, (filter) => {
      return filter.domains
    })
  }

  createFilters() {
    this.filters = this.axes.map(({ name, domains }) => {
      return {
        name,
        open: false,
        selected: false,
        domains: domains.map((domain) => {
          return { name: domain.name, id: domain.id, selected: false }
        }),
      }
    })
  }

  applyFilters(filters) {
    const selected = filters
      .map((filter) => {
        if (filter.selected) {
          return filter.id
        }
        return null
      })
      .filter((filter) => filter)
    if (selected.length > 0) {
      this.toShow = this[this.active].filter((item) => {
        return selected.includes(item.domain)
      })
    } else {
      this.toShow = this[this.active]
    }
  }

  clearFilters() {
    this.filters.forEach((filter) => {
      filter.selected = false
      filter.domains.forEach((domain) => {
        domain.selected = false
      })
    })
  }

  clearSearch() {
    this.searchText = null
  }

  activate(name) {
    if (typeof name === 'number') {
      name = [null, 'resources', 'lessons', 'experiences'][name]
    }
    const newName = name || window.location.hash.replace('#', '') || 'all'
    this.scope.$evalAsync(() => {
      this.active = newName
      this.applyFilters(this.extractDomainSelection())
      if (name) {
        // Frye the current hash if present and add the new one
        this.state.go(
          'cms',
          { '#': name },
          { location: 'replace', reloadOnSearch: false }
        )
      }
    })
  }

  toggleFilterGroup(group) {
    group.open = !group.open
  }

  toggleAll(group) {
    group.domains.forEach((checkbox) => {
      checkbox.selected = group.selected
    })
    if (group.selected) {
      group.open = true
    }
  }

  static factory() {
    require('../cms.scss')
    function planningAndGuidance($scope, $state, $ngRedux) {
      return new PlanningAndGuidanceController($scope, $state, $ngRedux)
    }
    planningAndGuidance.$inject = ['$scope', '$state', '$ngRedux']
    return planningAndGuidance
  }
}

export default PlanningAndGuidanceController
