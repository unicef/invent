import {
  stateGenerator,
  gettersGenerator,
  actionsGenerator,
  mutationsGenerator,
} from '../utilities/map'
import {
  intArrayFromQs,
  customColumnsMapper,
  strArrayFromQs,
  parseCustomAnswers,
} from '../utilities/api'

export const searchIn = () => [
  'name',
  'org',
  'overview',
  'partner',
  'donor',
  'loc',
]
export const defaultSelectedColumns = () => [
  '1',
  '2',
  '3',
  '4',
  '5',
  // '6',
  '7',
  '8',
  '10',
  '11',
  '12',
  '13',
  '14',
  '15',
  '18',
  '19',
  '20',
  '21',
  '22',
  '23',
  '24',
  '25',
  '26',
  '27',
  '40',
  '41',
]

export const state = () => ({
  ...stateGenerator(),
  searchIn: searchIn(),
  columns: [],
  selectedColumns: defaultSelectedColumns(),
  projectsList: [],
  projectsBucket: [],
  selectedDHI: [],
  selectedHFA: [],
  selectedHSC: [],
  selectedGoal: '',
  selectedResult: '',
  selectedCapabilityLevels: [],
  selectedCapabilityCategories: [],
  selectedCapabilitySubcategories: [],
  selectedPlatforms: [],
  selectedRows: [],
  innovationCategories: [],
  filteredCountries: [],
  filteredOffice: null,
  filteredCountryOffice: null,
  filteredRegion: null,
  selectAll: false,
  pageSize: 10,
  page: 1,
  total: 0,
  nextPage: 0,
  previousPage: 0,
  sorting: null,
  savedFilters: [],
  dashboardType: 'user',
  dashboardId: null,
  dashboardSection: 'map',
  regionalPriorities: [],
  sectors: [],
  filteredRegionalOffice: [],
  stage: null,
  innovationWays: [],
  hardwarePlatforms: [],
  programmePlatforms: [],
  platformFunctions: [],
  informationSecurity: null,
  // to track col with projects keys
  // we don't track these keys
  // approved
  // country_answers
  // country_custom_answers
  // country_custom_answers_private
  // donor_answers
  // donor_custom_answers
  // donor_custom_answers_private
  // favorite
  // hsc_challenges
  // id
  // innovation_categories
  // organisation
  mapColKeys: [
    { id: '1', label: 'Project name', key: 'name' },
    { id: '2', label: 'Country', key: 'country' },
    { id: '3', label: 'Last updated', key: 'modified' },
    { id: '4', label: 'Unicef Office', key: 'country_office' },
    { id: '5', label: 'Region', key: 'region' },
    // { id: '6', label: 'Investor', key: 'donors' },
    {
      id: '7',
      label: 'Programme Focal Point Name',
      key: ['contact_name', 'contact_email'],
    },
    {
      id: '8',
      label: 'Initiative Description',
      key: 'implementation_overview',
    },
    {
      id: '10',
      label: 'Health Focus Areas',
      key: 'health_focus_areas',
    },
    { id: '11', label: 'Goal Area', key: 'goal_area' },
    { id: '12', label: 'Result Area', key: 'result_area' },
    {
      id: '13',
      label: 'Capability Levels',
      key: 'capability_levels',
    },
    {
      id: '14',
      label: 'Capability Categories',
      key: 'capability_categories',
    },
    {
      id: '15',
      label: 'Capability Subcategories',
      key: 'capability_subcategories',
    },
    {
      id: '18',
      label: 'Multicountry or Regional Office',
      key: 'regional_office',
    },
    { id: '19', label: 'UNICEF Sector', key: 'unicef_sector' },
    {
      id: '20',
      label: 'Innovation Ways',
      key: 'innovation_ways',
    },
    { id: '21', label: 'Phase of Initiative', key: 'stages' },
    { id: '22', label: 'Hardware platform(s)', key: 'hardware' },
    {
      id: '23',
      label: 'Non-technology platform(s)',
      key: 'nontech',
    },
    {
      id: '24',
      label: 'Platform/Product Function',
      key: 'functions',
    },
    { id: '25', label: 'Information security classification', key: 'isc' },
    {
      id: '26',
      label: 'Regional priority(ies)',
      key: 'regional_priorities',
    },
    {
      id: '27',
      label: 'Software Platforms(s)',
      key: 'platforms',
    },
    {
      id: '40',
      label: 'Questionnaires Assigned',
      key: 'questionnaires_assigned',
    },
    { id: '41', label: 'Scoring', key: 'scoring' },
  ],
})
export const getters = {
  ...gettersGenerator(),
  getSearched: (state, getters) => {
    const g = getters.getSearchParameters
    return !(
      g.approved === undefined &&
      g.country.length === 0 &&
      g.dhi.length === 0 &&
      g.donor === null &&
      g.gov === undefined &&
      g.hfa.length === 0 &&
      g.goal === undefined &&
      g.result === undefined &&
      g.cl.length === 0 &&
      g.cc.length === 0 &&
      g.cs.length === 0 &&
      g.hsc.length === 0 &&
      g.ic.length === 0 &&
      g.in === undefined &&
      g.q === undefined &&
      g.region === null &&
      g.fo === null &&
      g.co === null &&
      g.sw.length === 0 &&
      g.view_as === undefined
    )
  },
  getProjectsList: (state) => [
    ...state.projectsList.map((r) => parseCustomAnswers(r)),
  ],
  getProjectsBucket: (state, getters) =>
    state.selectAll
      ? [...state.projectsBucket.map((r) => parseCustomAnswers(r))]
      : getters.getProjectsList,
  getCountryColumns: (state, getters, rootState, rootGetters) => {
    if (state.dashboardId && state.dashboardType === 'country') {
      const country = rootGetters['countries/getCountryDetails'](
        state.dashboardId
      )
      return country && country.country_questions
        ? customColumnsMapper(country.country_questions, 'c')
        : []
    }
    return []
  },
  getDonorColumns: (state, getters, rootState, rootGetters) => {
    if (state.dashboardId && state.dashboardType === 'donor') {
      const donor = rootGetters['system/getDonorDetails'](state.dashboardId)
      return donor && donor.donor_questions
        ? customColumnsMapper(donor.donor_questions, 'd')
        : []
    }
    return []
  },
  getAllColumns: (state, getters) => [
    ...state.columns,
    ...getters.getCountryColumns,
    ...getters.getDonorColumns,
  ],
  getAvailableColumns: (state, getters) => [
    ...getters.getAllColumns.map((c) => ({
      ...c,
      id: `${c.id}`,
      selected: state.selectedColumns.includes(`${c.id}`),
    })),
  ],
  getSelectedColumns: (state) => state.selectedColumns.map((s) => `${s}`),
  getSelectedDHI: (state) => state.selectedDHI,
  getSelectedHFA: (state) => state.selectedHFA,
  getSelectedHSC: (state) => state.selectedHSC,
  getSelectedGoal: (state) => state.selectedGoal,
  getSelectedResult: (state) => state.selectedResult,
  getSelectedPlatforms: (state) => state.selectedPlatforms,
  getSelectedCapabilityLevels: (state) => state.selectedCapabilityLevels,
  getSelectedCapabilityCategories: (state) =>
    state.selectedCapabilityCategories,
  getSelectedCapabilitySubcategories: (state) =>
    state.selectedCapabilitySubcategories,
  getSelectedRows: (state) => state.selectedRows,
  getFilteredCountries: (state) => {
    return state.dashboardType === 'country' && state.dashboardId
      ? [state.dashboardId]
      : state.filteredCountries
  },
  getFilteredRegion: (state) => state.filteredRegion,
  getFilteredOffice: (state) => state.filteredOffice,
  getFilteredCountryOffice: (state) => {
    return state.dashboardType === 'country' && state.dashboardId
      ? [state.dashboardId]
      : state.filteredCountryOffice
  },
  getFilteredRegionalOffice: (state) => {
    return state.filteredRegionalOffice
  },
  getUnicefSectors: (state) => state.sectors,
  getInnovationWays: (state) => state.innovationWays,
  getPhase: (state) => state.stage,
  getHardwarePlatforms: (state) => state.hardwarePlatforms,
  getProgrammePlatforms: (state) => state.programmePlatforms,
  getPlatformFunctions: (state) => state.platformFunctions,
  getInformationSecurity: (state) => state.informationSecurity,
  getInnovationCategories: (state) => state.innovationCategories,
  getRegionalPriorities: (state) => state.regionalPriorities,
  getGovernmentApproved: (state) => state.governmentApproved,
  getGovernmentFinanced: (state) => state.governmentFinanced,
  getSelectAll: (state) => state.selectAll,
  getPageSize: (state) => state.pageSize,
  getTotal: (state) => state.total,
  getNextPage: (state) => state.nextPage,
  getPreviousPage: (state) => state.previousPage,
  getCurrentPage: (state) => state.page,
  getSorting: (state) => state.sorting,
  getSavedFilters: (state) => state.savedFilters,
  getDashboardType: (state) => state.dashboardType,
  getDashboardId: (state) => state.dashboardId,
  getDashboardSection: (state) => state.dashboardSection,
  getSearchParameters: (state, getters) => {
    const q =
      state.searchString && state.searchString.length > 1
        ? state.searchString
        : ''
    const country = getters.getFilteredCountries
    const donor = state.dashboardType === 'donor' ? [state.dashboardId] : null
    return {
      page_size: state.pageSize,
      page: state.page,
      ordering: state.sorting,
      q,
      in: q ? state.searchIn : undefined,
      country,
      donor,
      region: state.filteredRegion ? state.filteredRegion : '',
      ic: state.innovationCategories,
      fo: state.filteredOffice,
      co: state.filteredCountryOffice,
      gov: state.governmentFinanced ? [1, 2] : undefined,
      approved: state.governmentApproved ? 1 : undefined,
      sw: state.selectedPlatforms,
      dhi: state.selectedDHI,
      hfa: state.selectedHFA,
      hsc: state.selectedHSC,
      goal: state.selectedGoal ? state.selectedGoal : '',
      result: state.selectedResult ? state.selectedResult : '',
      cl: state.selectedCapabilityLevels,
      cc: state.selectedCapabilityCategories,
      cs: state.selectedCapabilitySubcategories,
      view_as: state.dashboardType !== 'user' ? state.dashboardType : undefined,
      sc: state.selectedColumns,
      // new
      ro: state.filteredRegionalOffice,
      us: state.sectors,
      rp: state.regionalPriorities,
      iw: state.innovationWays,
      stage: state.stage,
      hp: state.hardwarePlatforms,
      pp: state.programmePlatforms,
      pf: state.platformFunctions,
      is: state.informationSecurity,
    }
  },
}

export const actions = {
  ...actionsGenerator(),
  setDashboardColumns({ commit }, columns) {
    commit('SET_DASHBOARD_COLUMNS', columns)
  },
  async loadProjectList({ rootState, rootGetters, commit, dispatch }) {
    const data = await dispatch('loadProjects', { type: 'list' })
    await dispatch('user/refreshProfile', {}, { root: true })
    const user = rootGetters['user/getProfile']
    const offices = rootState.offices.offices
    commit(
      'SET_PROJECT_LIST',
      data.results.projects.map((i) => {
        let regional_office = null
        if (i.country_office > 0) {
          const office = offices.find(({ id }) => id === i.country_office)
          regional_office = office ? office.regional_office : null
        }
        return {
          ...i,
          regional_office,
          favorite: user ? user.favorite.includes(i.id) : undefined,
        }
      })
    )
    commit('SET_SEARCH_STATUS', data)
    commit('SET_SELECT_ALL', false)
    commit('SET_SELECTED_ROWS', [])
    commit('SET_PROJECT_BUCKET', [])
  },
  async loadProjectsMap({ commit, dispatch }) {
    const data = await dispatch('loadProjects', {
      type: 'map',
      page_size: 999999,
      page: 1,
    })
    commit('SET_PROJECT_MAP', data.results.projects)
    commit('SET_SEARCH_STATUS', data)
  },
  async loadProjectsBucket({ commit, dispatch, state }) {
    if (state.projectsBucket.length === 0) {
      const data = await dispatch('loadProjects', {
        type: 'list',
        page_size: 999999,
        page: 1,
      })
      commit('SET_PROJECT_BUCKET', data.results.projects)
      commit('SET_SEARCH_STATUS', data)
    }
  },
  async setSearchOptions({ commit, dispatch }, options) {
    if (options.country && !Array.isArray(options.country)) {
      await dispatch('setSelectedCountry', +options.country)
      commit('SET_ACTIVE_COUNTRY', +options.country)
    }
    commit('SET_SEARCH_OPTIONS', options)
  },
  setSelectedColumns({ commit }, columns) {
    commit('SET_SELECTED_COLUMNS', columns)
  },
  setSearchString({ commit }, value) {
    commit('SET_SEARCH_STRING', value)
    commit('SET_CURRENT_PAGE', 1)
  },
  setSearchIn({ commit }, value) {
    commit('SET_SEARCH_IN', value)
    commit('SET_CURRENT_PAGE', 1)
  },
  setSelectedDHI({ commit, dispatch }, columns) {
    dispatch('setSearchGoals', { key: 'dhi', val: columns })
    commit('SET_SELECTED_DHI', columns)
    commit('SET_CURRENT_PAGE', 1)
  },
  setSelectedHFA({ commit, dispatch }, columns) {
    dispatch('setSearchGoals', { key: 'hfa', val: columns })
    commit('SET_SELECTED_HFA', columns)
    commit('SET_CURRENT_PAGE', 1)
  },
  setSelectedHSC({ commit, dispatch }, columns) {
    dispatch('setSearchGoals', { key: 'hsc', val: columns })
    commit('SET_SELECTED_HSC', columns)
    commit('SET_CURRENT_PAGE', 1)
  },
  setSelectedGoal({ commit }, columns) {
    commit('SET_SELECTED_GOAL', columns)
    commit('SET_CURRENT_PAGE', 1)
  },
  setSelectedResult({ commit }, columns) {
    commit('SET_SELECTED_RESULT', columns)
    commit('SET_CURRENT_PAGE', 1)
  },
  setSelectedCapabilityLevels({ commit, dispatch }, columns) {
    dispatch('setSearchGoals', { key: 'cl', val: columns })
    commit('SET_SELECTED_CAPABILITY_LEVELS', columns)
    commit('SET_CURRENT_PAGE', 1)
  },
  setSelectedCapabilityCategories({ commit, dispatch }, columns) {
    dispatch('setSearchGoals', { key: 'cc', val: columns })
    commit('SET_SELECTED_CAPABILITY_CATEGORIES', columns)
    commit('SET_CURRENT_PAGE', 1)
  },
  setSelectedCapabilitySubcategories({ commit, dispatch }, columns) {
    dispatch('setSearchGoals', { key: 'cs', val: columns })
    commit('SET_SELECTED_CAPABILITY_SUBCATEGORIES', columns)
    commit('SET_CURRENT_PAGE', 1)
  },
  setSelectedPlatforms({ commit, dispatch }, columns) {
    dispatch('setSearchGoals', { key: 'sw', val: columns })
    commit('SET_SELECTED_PLATFORMS', columns)
    commit('SET_CURRENT_PAGE', 1)
  },
  setSearchGoals({ commit, dispatch, rootState }, { key, val }) {
    if (!rootState.search.blockSearch) {
      commit('search/SET_SEARCH', { key: 'sw', val }, { root: true })
      dispatch('search/getSearch', {}, { root: true })
    }
  },
  setSelectedRows({ commit, state }, rows) {
    if (state.selectAll && state.selectedRows.length > rows.length) {
      commit('SET_SELECT_ALL', false)
    }
    commit('SET_SELECTED_ROWS', rows)
  },
  async setFilteredCountries({ commit, dispatch }, value) {
    if (value && value.length === 1) {
      await dispatch('setSelectedCountry', value[0])
      commit('SET_ACTIVE_COUNTRY', value[0])
    } else if (value && (value.length > 0 || value.length === 0)) {
      commit('SET_SELECTED_COUNTRY', null)
      commit('SET_ACTIVE_COUNTRY', null)
    }
    commit('SET_FILTERED_COUNTRIES', value)
    commit('SET_CURRENT_PAGE', 1)
  },
  setFilteredRegion({ commit }, value) {
    commit('SET_FILTERED_REGION', value)
    commit('SET_CURRENT_PAGE', 1)
  },
  setFilteredRegionalOffice({ commit }, value) {
    commit('SET_FILTERED_REGIONAL_OFFICE', value)
    commit('SET_CURRENT_PAGE', 1)
  },
  setUnicefSectors({ commit }, value) {
    commit('SET_UNICEF_SECTORS', value)
    commit('SET_CURRENT_PAGE', 1)
  },
  setInnovationCategories({ commit }, value) {
    commit('SET_INNOVATION_CATEGORIES', value)
    commit('SET_CURRENT_PAGE', 1)
  },
  setRegionalPriorities({ commit }, value) {
    commit('SET_REGIONAL_PRIORITIES', value)
    commit('SET_CURRENT_PAGE', 1)
  },
  setInnovationWays({ commit }, value) {
    commit('SET_DATA', { type: 'innovationWays', value })
    commit('SET_CURRENT_PAGE', 1)
  },
  setPhase({ commit }, value) {
    commit('SET_DATA', { type: 'stage', value })
    commit('SET_CURRENT_PAGE', 1)
  },
  setHardwarePlatforms({ commit }, value) {
    commit('SET_DATA', { type: 'hardwarePlatforms', value })
    commit('SET_CURRENT_PAGE', 1)
  },
  setProgrammePlatforms({ commit }, value) {
    commit('SET_DATA', { type: 'programmePlatforms', value })
    commit('SET_CURRENT_PAGE', 1)
  },
  setPlatformFunctions({ commit }, value) {
    commit('SET_DATA', { type: 'platformFunctions', value })
    commit('SET_CURRENT_PAGE', 1)
  },
  setInformationSecurity({ commit }, value) {
    commit('SET_DATA', { type: 'informationSecurity', value })
    commit('SET_CURRENT_PAGE', 1)
  },
  setFilteredOffice({ commit }, value) {
    commit('SET_FILTERED_OFFICE', value)
    commit('SET_CURRENT_PAGE', 1)
  },
  setFilteredCountryOffice({ commit }, value) {
    commit('SET_FILTERED_COUNTRY_OFFICE', value)
    commit('SET_CURRENT_PAGE', 1)
  },
  setGovernmentApproved({ commit }, value) {
    commit('SET_GOVERNMENT_APPROVED', value)
    commit('SET_CURRENT_PAGE', 1)
  },
  setGovernmentFinanced({ commit }, value) {
    commit('SET_GOVERNMENT_FINANCED', value)
    commit('SET_CURRENT_PAGE', 1)
  },
  setSelectAll({ commit }, all) {
    commit('SET_SELECT_ALL', all)
  },
  setPageSize({ commit }, size) {
    commit('SET_PAGE_SIZE', size)
    commit('SET_CURRENT_PAGE', 1)
  },
  setCurrentPage({ commit }, page) {
    commit('SET_CURRENT_PAGE', page)
  },
  setSorting({ commit }, value) {
    commit('SET_SORTING', value)
    commit('SET_CURRENT_PAGE', 1)
  },
  setSavedFilters({ commit }, filters) {
    if (window && window.localStorage) {
      window.localStorage.setItem('savedFilters', JSON.stringify(filters))
    }
    commit('SET_SAVED_FILTERS', filters)
  },
  async setDashboardType({ commit, dispatch, getters }, { type, id }) {
    commit('SET_SEARCH_OPTIONS', {
      view_as: type,
      donor: type === 'donor' ? id : undefined,
      country: type === 'country' ? [id] : undefined,
    })
    const selectedColumns = [...getters.getSelectedColumns]
    if (type === 'country') {
      selectedColumns.push(...getters.getCountryColumns.map((cc) => cc.id))
      await dispatch('setSelectedCountry', id)
      commit('SET_ACTIVE_COUNTRY', id)
    } else if (type === 'donor') {
      await dispatch('system/loadDonorDetails', getters.getDashboardId, {
        root: true,
      })
      selectedColumns.push(...getters.getDonorColumns.map((cc) => cc.id))
    }
    commit('SET_PROJECT_BUCKET', [])
    commit('SET_SELECTED_COLUMNS', selectedColumns)
  },
  setDashboardSection({ commit }, value) {
    commit('SET_DASHBOARD_SECTION', value)
  },
  resetUserInput({ state, commit, dispatch }) {
    commit('RESET_USER_INPUT')
    commit('SET_SEARCH_OPTIONS', {})
    commit('SET_SELECTED_COLUMNS', defaultSelectedColumns())
  },
}
export const mutations = {
  ...mutationsGenerator(),
  SET_DASHBOARD_COLUMNS: (state, columns) => {
    state.columns = [
      ...columns,
      // todo: set this columns on the backend
      { id: 27, label: 'Software Platforms(s)' },
      { id: 40, label: 'Questionnaires Assigned' },
      { id: 41, label: 'Scoring' },
    ]
  },
  SET_PROJECT_LIST: (state, projects) => {
    state.projectsList = projects.map((i) => {
      return {
        ...i,
      }
    })
  },
  SET_PROJECT_BUCKET: (state, projects) => {
    state.projectsBucket = projects
  },
  SET_SEARCH_OPTIONS: (state, options) => {
    state.pageSize = options.page_size ? +options.page_size : 10
    state.page = options.page ? +options.page : 1
    state.sorting = options.ordering ? options.ordering : null
    state.searchString = options.q ? options.q : ''
    state.searchIn = options.in ? options.in : searchIn()
    state.filteredCountries = intArrayFromQs(options.country)
    state.innovationCategories = intArrayFromQs(options.ic)
    state.filteredRegion = options.region ? +options.region : null
    state.filteredOffice = options.fo ? +options.fo : null
    state.filteredCountryOffice = intArrayFromQs(options.co)
    state.governmentFinanced = options.gov ? true : null
    state.governmentApproved = options.approved ? true : null
    state.selectedPlatforms = intArrayFromQs(options.sw)

    state.regionalPriorities = intArrayFromQs(options.rp)
    state.sectors = intArrayFromQs(options.us)
    state.filteredRegionalOffice = intArrayFromQs(options.ro)
    state.innovationWays = intArrayFromQs(options.iw)
    state.hardwarePlatforms = intArrayFromQs(options.hp)
    state.programmePlatforms = intArrayFromQs(options.pp)
    state.platformFunctions = intArrayFromQs(options.pf)
    state.stage = options.pi ? +options.pi : null
    state.informationSecurity = options.is ? +options.is : null

    state.selectedDHI = intArrayFromQs(options.dhi)
    state.selectedHFA = intArrayFromQs(options.hfa)
    state.selectedHSC = intArrayFromQs(options.hsc)
    state.selectedGoal = options.goal ? +options.goal : null
    state.selectedResult = options.result ? +options.result : null
    state.selectedCapabilityLevels = intArrayFromQs(options.cl)
    state.selectedCapabilityCategories = intArrayFromQs(options.cc)
    state.selectedCapabilitySubcategories = intArrayFromQs(options.cs)
    state.selectedColumns = options.sc
      ? strArrayFromQs(options.sc)
      : defaultSelectedColumns()
    state.dashboardType = options.view_as ? options.view_as : 'user'
    state.dashboardId =
      options.view_as === 'country'
        ? intArrayFromQs(options.country)[0]
        : options.view_as === 'donor'
        ? +options.donor
        : null
  },
  SET_SELECTED_COLUMNS: (state, columns) => {
    state.selectedColumns = columns
  },
  SET_SELECTED_DHI: (state, dhi) => {
    state.selectedDHI = dhi
  },
  SET_SELECTED_HFA: (state, hfa) => {
    state.selectedHFA = hfa
  },
  SET_SELECTED_HSC: (state, hsc) => {
    state.selectedHSC = hsc
  },
  SET_SELECTED_GOAL: (state, goal) => {
    state.selectedGoal = goal || null
  },
  SET_SELECTED_RESULT: (state, result) => {
    state.selectedResult = result || null
  },
  SET_SELECTED_CAPABILITY_LEVELS: (state, cl) => {
    state.selectedCapabilityLevels = cl
  },
  SET_SELECTED_CAPABILITY_CATEGORIES: (state, cc) => {
    state.selectedCapabilityCategories = cc
  },
  SET_SELECTED_CAPABILITY_SUBCATEGORIES: (state, cs) => {
    state.selectedCapabilitySubcategories = cs
  },
  SET_SELECTED_PLATFORMS: (state, platforms) => {
    state.selectedPlatforms = platforms
  },
  SET_SELECTED_ROWS: (state, rows) => {
    state.selectedRows = rows
  },
  SET_FILTERED_COUNTRIES: (state, value) => {
    state.filteredCountries = value
  },
  SET_FILTERED_OFFICE: (state, value) => {
    state.filteredOffice = value
  },
  SET_FILTERED_COUNTRY_OFFICE: (state, value) => {
    state.filteredCountryOffice = value
  },
  SET_FILTERED_REGION: (state, value) => {
    state.filteredRegion = value
  },
  SET_FILTERED_REGIONAL_OFFICE: (state, value) => {
    state.filteredRegionalOffice = value
  },
  SET_UNICEF_SECTORS: (state, value) => {
    state.sectors = value
  },
  SET_INNOVATION_CATEGORIES: (state, value) => {
    state.innovationCategories = value
  },
  SET_REGIONAL_PRIORITIES: (state, value) => {
    state.regionalPriorities = value
  },
  SET_GOVERNMENT_APPROVED: (state, value) => {
    state.governmentApproved = value
  },
  SET_GOVERNMENT_FINANCED: (state, value) => {
    state.governmentFinanced = value
  },
  SET_SELECT_ALL: (state, all) => {
    state.selectAll = all
  },
  SET_PAGE_SIZE: (state, size) => {
    state.pageSize = size
  },
  SET_CURRENT_PAGE: (state, page) => {
    state.page = page
  },
  SET_SORTING: (state, value) => {
    state.sorting = value
  },
  SET_SEARCH_STATUS: (state, status) => {
    state.total = status.count
    state.nextPage = status.next
    state.previousPage = status.previous
  },
  SET_SAVED_FILTERS: (state, filters) => {
    state.savedFilters = filters
  },
  SET_DASHBOARD_TYPE: (state, { type, id }) => {
    state.dashboardType = type
    state.dashboardId = id
  },
  SET_DASHBOARD_SECTION: (state, section) => {
    state.dashboardSection = section
  },
  SET_DATA: (state, { type, value }) => {
    state[type] = value
  },
}
