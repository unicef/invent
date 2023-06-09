import isEmpty from 'lodash/isEmpty'
import get from 'lodash/get'

export const state = () => ({
  landingProjects: [],
  userProjects: [],
  currentProject: null,
  projectStructure: {},
  // initiatives tabs
  tabs: [
    { id: 1, name: 'My initiatives', icon: 'star', total: 1 },
    { id: 4, name: 'Country focal point', icon: 'globe-africa', total: 1 },
    { id: 2, name: 'My reviews', icon: 'comment-alt', total: 1 },
    { id: 3, name: 'My favorites', icon: 'heart', total: 1 },
  ],
  tab: 1,
  loadingProject: true,
  pageSize: 10,
  page: 1,
  total: 0,
  nextPage: 0,
  previousPage: 0,
  // project review
  loadingReview: false,
  dialogReview: false,
  errorReview: false,
  currentProjectReview: {},
  problemStatements: [],
})

const getTodayString = () => {
  const today = new Date()
  const year = today.getFullYear()
  const month = ('0' + (today.getMonth() + 1)).slice(-2)
  const day = ('0' + today.getDate()).slice(-2)

  return [year, month, day].join('-')
}

export const getters = {
  getLandingProjects: (state) => state.landingProjects,
  getUserProjectList: (state) => [...state.userProjects.map((p) => ({ ...p }))],
  getGoalAreas: (state) => get(state, 'projectStructure.goal_areas', []),
  getRegionalOffices: (state) => get(state, 'projectStructure.regional_offices', []),
  getResultAreas: (state) => get(state, 'projectStructure.result_areas', []),
  getCapabilityLevels: (state) => (id) => {
    const all = get(state, 'projectStructure.capability_levels', [])
    return id ? all.filter((i) => i.goal_area_id === id) : all
  },
  getCapabilityCategories: (state) => (id) => {
    const all = get(state, 'projectStructure.capability_categories', [])
    return id ? all.filter((i) => i.goal_area_id === id) : all
  },
  getCapabilitySubcategories: (state) => (id) => {
    const all = get(state, 'projectStructure.capability_subcategories', [])
    return id ? all.filter((i) => i.goal_area_id === id) : all
  },
  getHealthFocusAreas: (state) =>
    state.projectStructure.health_focus_areas ? [...state.projectStructure.health_focus_areas] : [],
  getHisBucket: (state) => (state.projectStructure.his_bucket ? [...state.projectStructure.his_bucket] : []),
  getHscChallenges: (state) =>
    state.projectStructure.hsc_challenges ? [...state.projectStructure.hsc_challenges] : [],
  getInteroperabilityLinks: (state) =>
    state.projectStructure.interoperability_links ? [...state.projectStructure.interoperability_links] : [],
  getInteroperabilityStandards: (state) =>
    state.projectStructure.interoperability_standards ? [...state.projectStructure.interoperability_standards] : [],
  getLicenses: (state) => (state.projectStructure.licenses ? [...state.projectStructure.licenses] : []),
  getDigitalHealthInterventions: (state) =>
    state.projectStructure.strategies ? [...state.projectStructure.strategies] : [],
  getDigitalHealthInterventionDetails: (state, getters) => (id) => {
    for (const category of getters.getDigitalHealthInterventions) {
      for (const group of category.subGroups) {
        const result = group.strategies.find((s) => s.id === id)
        if (result) {
          return result
        }
      }
    }
  },
  getTechnologyPlatforms: (state) =>
    state.projectStructure.technology_platforms ? [...state.projectStructure.technology_platforms] : [],
  getSectors: (state) => (state.projectStructure.sectors ? [...state.projectStructure.sectors] : []),
  getLeadingSector: (state, getters, rootState, rootGetters) => {
    const selectedSupportingSectors = rootGetters['project/getSupportingSectors']
    const sectors = state.projectStructure.sectors
    const remainingSectors = sectors.map((sector) =>
      selectedSupportingSectors.some((selSector) => selSector === sector.id)
        ? { ...sector, disabled: true, value: sector.id }
        : { ...sector, disabled: false, value: sector.id }
    )

    return remainingSectors
  },
  getSupportingSectors: (state, getters, rootState, rootGetters) => {
    const selectedLeadingSectors = rootGetters['project/getLeadingSector']
    const sectors = state.projectStructure.sectors
    const remainingSectors = sectors.map((sector) =>
      selectedLeadingSectors.some((selSector) => selSector === sector.id)
        ? { ...sector, disabled: true, value: sector.id }
        : { ...sector, disabled: false, value: sector.id }
    )

    return remainingSectors
  },
  getInfoSec: (state) => (state.projectStructure.isc ? [...state.projectStructure.isc] : []),
  getInnovationWays: (state) =>
    state.projectStructure.innovation_ways ? [...state.projectStructure.innovation_ways] : [],
  getRegionalPriorities: (state) =>
    state.projectStructure.regional_priorities ? [...state.projectStructure.regional_priorities] : [],
  getHardware: (state) => (state.projectStructure.hardware ? [...state.projectStructure.hardware] : []),
  getNontech: (state) => (state.projectStructure.nontech ? [...state.projectStructure.nontech] : []),
  getFunctions: (state) => (state.projectStructure.functions ? [...state.projectStructure.functions] : []),
  getCurrencies: (state) => (state.projectStructure.currencies ? [...state.projectStructure.currencies] : []),
  getPhases: (state) => (state.projectStructure.phases ? [...state.projectStructure.phases] : []),
  getStages: (state) => (state.projectStructure.stages ? [...state.projectStructure.stages] : []),
  getCpd: (state) => (state.projectStructure.cpd ? [...state.projectStructure.cpd] : []),
  getInnovationCategories: (state) =>
    state.projectStructure.innovation_categories ? [...state.projectStructure.innovation_categories] : [],
  getProjectDetails: (state, getters, rootState, rootGetters) => (p) => {
    if (p) {
      const user = rootGetters['user/getProfile']
      return {
        ...p,
        isMember: user ? user.member.includes(p.id) : undefined,
        isViewer: user ? user.viewer.includes(p.id) : undefined,
        isPublished: !!(p.published && p.published.name),
      }
    }
    return {}
  },
  getUserProjectDetails: (state, getters, rootState, rootGetters) => (id) => {
    const p = getters.getUserProjectList.find((p) => p.id === id)
    return getters.getProjectDetails(p)
  },
  getCurrentProject: (state, getters, rootState, rootGetters) => {
    // Utility method for retro-compatibility
    const p = rootGetters['project/getOriginal']
    return getters.getProjectDetails(p)
  },
  getPageSize: (state) => state.pageSize,
  getTotal: (state) => state.total,
  getCurrentPage: (state) => state.page,
}

export const actions = {
  async loadLandingProjects({ commit, rootGetters, dispatch }) {
    try {
      const { data } = await this.$axios.get('/api/projects/landing/')
      const regions = rootGetters['system/getRegions']
      let countries = rootGetters['countries/getCountries']
      if (countries.length === 0) {
        await dispatch('countries/loadMapData', {}, { root: true })
        countries = rootGetters['countries/getCountries']
      }
      countries.map((c) => {
        return {
          ...c,
          unicef_region: regions.find((r) => r.id === c.unicef_region),
        }
      })
      const offices = rootGetters['offices/getOffices'].map((o) => {
        return {
          ...o,
          region: regions.find((r) => r.id === o.region),
        }
      })

      const my_initiatives = data.my_initiatives.map((p) => {
        return {
          ...p,
          country: countries.find((c) => c.id === p.country),
          unicef_office: offices.find((o) => o.id === p.unicef_office),
        }
      })

      const recents = data.recents.map((p) => {
        return {
          ...p,
          country: countries.find((c) => c.id === p.country),
          unicef_office: offices.find((o) => o.id === p.unicef_office),
        }
      })

      const featured = data.featured.map((p) => {
        return {
          ...p,
          country: countries.find((c) => c.id === p.country),
          unicef_office: offices.find((o) => o.id === p.unicef_office),
        }
      })
      commit('SET_VALUE', {
        key: 'landingProjects',
        val: {
          my_initiatives_count: data.my_initiatives_count,
          my_initiatives,
          recents,
          featured,
        },
      })
    } catch (error) {
      console.error('projects/landing failed')
      return Promise.reject(error)
    }
  },
  async loadUserProjects({ commit }) {
    try {
      const { data } = await this.$axios.get('/api/projects/user-list/member-of/')
      data.results.sort((a, b) => b.id - a.id)
      commit('SET_USER_PROJECT_LIST', data.results)
    } catch (error) {
      console.error('projects/loadUserProjects failed')
      return Promise.reject(error)
    }
  },
  async getInitiatives({ state, commit, dispatch, rootGetters }, itemsOnPage = 0) {
    commit('SET_VALUE', { key: 'loadingProject', val: true })
    commit('SET_VALUE', { key: 'userProjects', val: [] })
    await dispatch('offices/loadOffices', {}, { root: true })
    await dispatch('user/refreshProfile', {}, { root: true })
    const user = rootGetters['user/getProfile']
    let reviewPage = 1
    let initiativePage = 1
    let favoritesPages = 1
    let countryManagerPages = 1
    switch (state.tab) {
      case 1:
        initiativePage = state.page
        break
      case 2:
        reviewPage = state.page
        break
      case 3:
        favoritesPages = itemsOnPage === 1 && state.page > 1 ? state.page - 1 : state.page
        break
      case 4:
        countryManagerPages = itemsOnPage === 1 && state.page > 1 ? state.page - 1 : state.page
        break
    }
    try {
      const results = await Promise.all([
        this.$axios.get(`/api/projects/user-list/member-of/?page_size=${state.pageSize}&page=${initiativePage}`),
        this.$axios.get(`/api/projects/user-list/review/?page_size=${state.pageSize}&page=${reviewPage}`),
        this.$axios.get(`/api/projects/user-list/favorite/?page_size=${state.pageSize}&page=${favoritesPages}`),
        this.$axios.get(
          `/api/projects/user-list/country-manager/?page_size=${state.pageSize}&page=${countryManagerPages}`
        ),
      ])
      // for review case
      if (state.tab === 2) {
        let { data } = results[state.tab - 1]
        commit('SET_VALUE', { key: 'total', val: data.count })
        data.results.sort((a, b) => b.id - a.id)
        data = data.results.map((p) => {
          const project = p.project
          const office = rootGetters['offices/getOfficeDetails'](project.country_office)
          const isCountryManager = office.managers.findIndex((m) => m.id === user.id) > -1
          return {
            reviewId: p.id,
            ...p,
            ...project,
            favorite: user ? user.favorite.includes(p.project.id) : undefined,
            isMember: user ? user.member.includes(p.id) || isCountryManager : undefined,
            isViewer: user ? user.viewer.includes(p.id) : undefined,
            isPublished: true,
          }
        })
        commit('SET_VALUE', { key: 'userProjects', val: data })
      } else {
        let { data } = results[state.tab - 1]
        commit('SET_VALUE', { key: 'total', val: data.count })
        data.results.sort((a, b) => b.id - a.id)
        data = data.results.map((p) => {
          const project = p.public_id ? p.published : p.draft
          const office = rootGetters['offices/getOfficeDetails'](project.country_office)
          const isCountryManager = office.managers.findIndex((m) => m.id === user.id) > -1
          return {
            ...p,
            ...project,
            favorite: user ? user.favorite.includes(p.id) : undefined,
            isMember: user ? user.member.includes(p.id) || isCountryManager : undefined,
            isViewer: user ? user.viewer.includes(p.id) : undefined,
            isPublished: !!p.public_id,
          }
        })
        commit('SET_VALUE', { key: 'userProjects', val: data })
      }
      // update tab counts
      commit('SET_VALUE', {
        key: 'tabs',
        val: [
          {
            id: 1,
            name: 'My initiatives',
            icon: 'star',
            total: results[0].data.count,
          },
          {
            id: 4,
            name: 'Country focal point',
            icon: 'globe-africa',
            total: results[3].data.count,
          },
          {
            id: 2,
            name: 'My reviews',
            icon: 'comment-alt',
            total: results[1].data.count,
          },
          {
            id: 3,
            name: 'My favorites',
            icon: 'heart',
            total: results[2].data.count,
          },
        ],
      })
      commit('SET_VALUE', { key: 'loadingProject', val: false })
    } catch (e) {
      console.error('portfolio/loadPortfolioProjects failed', e.response)
      commit('SET_VALUE', { key: 'loadingProject', val: false })
    }
  },
  async addReview({ state, commit, dispatch }, { id, ...score }) {
    try {
      commit('SET_VALUE', { key: 'loadingReview', val: true })
      commit('SET_VALUE', { key: 'errorReview', val: false })
      await this.$axios.post(`/api/project-review/${id}/fill/`, {
        ...score,
      })
      // update initiatives
      dispatch('getInitiatives')
      // interface setters
      commit('SET_VALUE', { key: 'loadingReview', val: false })
      commit('SET_VALUE', { key: 'dialogReview', val: false })
    } catch (e) {
      commit('SET_VALUE', { key: 'loadingReview', val: false })
      commit('SET_VALUE', { key: 'errorReview', val: true })
    }
  },
  setCurrentProject({ commit, dispatch }, id) {
    id = parseInt(id, 10)
    commit('SET_CURRENT_PROJECT', id)
  },
  async snapShotProject({ state, dispatch }) {
    const id = state.currentProject
    await this.$axios.post(`/api/projects/${id}/version/`)
    return dispatch('loadProjectDetails', id)
  },
  async loadProjectStructure({ state, commit }, force) {
    try {
      const structure = state.projectStructure
      if (isEmpty(structure) || force) {
        const { data } = await this.$axios.get('/api/projects/structure/')
        commit('SET_PROJECT_STRUCTURE', data)
      }
    } catch (e) {
      console.error('projects/loadProjectStructure failed')
    }
  },
  addProjectToList({ commit }, project) {
    commit('ADD_USER_PROJECT', project)
  },
  updateProject({ commit }, project) {
    commit('EDIT_USER_PROJECT', project)
  },
  removeProject({ commit }, id) {
    commit('RM_USER_PROJECT', id)
  },
  resetProjectsData({ commit }) {
    commit('RESET_PROJECTS_DATA')
  },
  // get every project or initiative
  async setTab({ state, commit, dispatch }, val) {
    commit('SET_VALUE', { key: 'tab', val })
    commit('SET_VALUE', { key: 'page', val: 1 })
    await dispatch('getInitiatives')
  },
  addFavorite({ state, commit, dispatch }, { id, type }) {
    dispatch('setFavorite', { id, type, action: 'add' })
  },
  removeFavorite({ state, commit, dispatch }, { id, type }) {
    dispatch('setFavorite', { id, type, action: 'remove' })
  },
  async setFavorite({ state, commit, dispatch }, { id, type, action }) {
    try {
      await this.$axios.put(`/api/projects/favorites/${action}/${id}`)
      switch (type) {
        case 'initiatives':
          await dispatch('getInitiatives', state.userProjects.length)
          break
        case 'inventory':
          await dispatch('dashboard/loadProjectList', {}, { root: true })
          break
        case 'table':
          await dispatch('search/getSearch', {}, { root: true })
          break
        case 'detail':
          await dispatch('user/refreshProfile', {}, { root: true })
          break
      }
    } catch (e) {
      console.log(e.response.data)
    }
  },
  async setNewItem({ commit, dispatch }, { type, name }) {
    try {
      const { data } = await this.$axios.post(`/api/projects/${type}-request/`, { name })
      await dispatch('loadProjectStructure', true)
      return data.id
    } catch (e) {
      return e
    }
  },
  // state interaction handlers
  setCurrentProjectReview({ commit }, val) {
    commit('SET_VALUE', { key: 'currentProjectReview', val })
  },
  setReviewDialog({ commit }, val) {
    commit('SET_VALUE', { key: 'dialogReview', val })
  },
  setPageSize({ commit, dispatch }, size) {
    if (process.browser) {
      localStorage.setItem('pageSize', size)
    }
    commit('SET_VALUE', { key: 'pageSize', val: size })
    commit('SET_VALUE', { key: 'page', val: 1 })
    dispatch('getInitiatives')
  },
  restorePageSize({ commit }) {
    let pageSize = 10
    if (process.browser) {
      const lsPageSize = localStorage.getItem('pageSize')
      pageSize = lsPageSize ? parseInt(lsPageSize) : 10
    }
    commit('SET_VALUE', { key: 'pageSize', val: pageSize })
    commit('SET_VALUE', { key: 'page', val: 1 })
  },
  setCurrentPage({ commit, dispatch }, page) {
    commit('SET_VALUE', { key: 'page', val: page })
    dispatch('getInitiatives')
  },
}

export const mutations = {
  SET_VALUE(state, { key, val }) {
    state[key] = val
  },
  SET_USER_PROJECT_LIST: (state, projects) => {
    state.userProjects = projects
  },
  ADD_USER_PROJECT: (state, project) => {
    state.userProjects.push(project)
  },
  EDIT_USER_PROJECT: (state, project) => {
    const index = state.userProjects.findIndex((p) => p.id === project.id)
    state.userProjects.splice(index, 1, project)
  },
  RM_USER_PROJECT: (state, id) => {
    state.userProjects = state.userProjects.filter((p) => p.id !== id)
  },
  SET_CURRENT_PROJECT: (state, project) => {
    state.currentProject = project
  },
  SET_PROJECT_STRUCTURE: (state, structure) => {
    state.projectStructure = structure
  },
  RESET_PROJECTS_DATA: (state) => {
    state.userProjects = []
    state.currentProject = null
    state.projectStructure = {}
  },
}
