import isEmpty from 'lodash/isEmpty'
import forOwn from 'lodash/forOwn'
import get from 'lodash/get'

export const state = () => ({
  userProjects: [],
  currentProject: null,
  projectStructure: {},
  currentProjectToolkitVersions: [],
  currentProjectCoverageVersions: [],
  // initiatives tabs
  tabs: [
    { id: 1, name: 'My initiatives', icon: 'star', total: 1 },
    { id: 2, name: 'My reviews', icon: 'comment-alt', total: 1 },
    { id: 3, name: 'My favorites', icon: 'heart', total: 1 },
  ],
  tab: 1,
  loadingProject: true,
  // project review
  loadingReview: false,
  dialogReview: false,
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
  getUserProjectList: (state) => [...state.userProjects.map((p) => ({ ...p }))],
  getGoalAreas: (state) => get(state, 'projectStructure.goal_areas', []),
  getRegionalOffices: (state) =>
    get(state, 'projectStructure.regional_offices', []),
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
    state.projectStructure.health_focus_areas
      ? [...state.projectStructure.health_focus_areas]
      : [],
  getHisBucket: (state) =>
    state.projectStructure.his_bucket
      ? [...state.projectStructure.his_bucket]
      : [],
  getHscChallenges: (state) =>
    state.projectStructure.hsc_challenges
      ? [...state.projectStructure.hsc_challenges]
      : [],
  getInteroperabilityLinks: (state) =>
    state.projectStructure.interoperability_links
      ? [...state.projectStructure.interoperability_links]
      : [],
  getInteroperabilityStandards: (state) =>
    state.projectStructure.interoperability_standards
      ? [...state.projectStructure.interoperability_standards]
      : [],
  getLicenses: (state) =>
    state.projectStructure.licenses ? [...state.projectStructure.licenses] : [],
  getDigitalHealthInterventions: (state) =>
    state.projectStructure.strategies
      ? [...state.projectStructure.strategies]
      : [],
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
    state.projectStructure.technology_platforms
      ? [...state.projectStructure.technology_platforms]
      : [],
  getSectors: (state) =>
    state.projectStructure.sectors ? [...state.projectStructure.sectors] : [],
  getRegionalPriorities: (state) =>
    state.projectStructure.regional_priorities
      ? [...state.projectStructure.regional_priorities]
      : [],
  getHardware: (state) =>
    state.projectStructure.hardware ? [...state.projectStructure.hardware] : [],
  getNontech: (state) =>
    state.projectStructure.nontech ? [...state.projectStructure.nontech] : [],
  getFunctions: (state) =>
    state.projectStructure.functions
      ? [...state.projectStructure.functions]
      : [],
  getCurrencies: (state) =>
    state.projectStructure.currencies
      ? [...state.projectStructure.currencies]
      : [],
  getPhases: (state) =>
    state.projectStructure.phases ? [...state.projectStructure.phases] : [],
  getCpd: (state) =>
    state.projectStructure.cpd ? [...state.projectStructure.cpd] : [],
  getInnovationCategories: (state) =>
    state.projectStructure.innovation_categories
      ? [...state.projectStructure.innovation_categories]
      : [],
  getToolkitVersions: (state) => [...state.currentProjectToolkitVersions],
  getCoverageVersions: (state) => [...state.currentProjectCoverageVersions],
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
  getMapsAxisData: (state, getters, rootState, rootGetters) => {
    const axis = rootGetters['system/getAxis']
    const chartAxis = { labels: axis.map((a) => a.name), data: [] }
    const toolkitVersion = getters.getToolkitVersions
    const toolkitData = rootGetters['toolkit/getToolkitData']
    const todayString = getTodayString()
    if (toolkitVersion.length > 0) {
      // Data from versions
      chartAxis.data = toolkitVersion.map((version) => {
        return {
          date: version.modified.split('T')[0],
          axis1: version.data[0].axis_score / 100,
          axis2: version.data[1].axis_score / 100,
          axis3: version.data[2].axis_score / 100,
          axis4: version.data[3].axis_score / 100,
          axis5: version.data[4].axis_score / 100,
          axis6: version.data[5].axis_score / 100,
        }
      })
    }

    // Current data (from tooltip)

    if (toolkitData.length === 6) {
      const lastAxisData = {
        axis1: toolkitData[0].axis_score / 100,
        axis2: toolkitData[1].axis_score / 100,
        axis3: toolkitData[2].axis_score / 100,
        axis4: toolkitData[3].axis_score / 100,
        axis5: toolkitData[4].axis_score / 100,
        axis6: toolkitData[5].axis_score / 100,
        date: todayString,
      }
      chartAxis.data.push(lastAxisData)
    }
    return chartAxis
  },
  getMapsDomainData: (state, getters, rootState, rootGetters) => {
    const domains = rootGetters['system/getDomains']
    const axes = rootGetters['system/getAxis']
    const chartData = { labels: axes.map((a) => a.name) }
    const toolkitVersion = getters.getToolkitVersions
    const toolkitData = rootGetters['toolkit/getToolkitData']
    const todayString = getTodayString()
    axes.forEach((axis, axInd) => {
      chartData[axis.name] = {
        labels: domains.filter((d) => d.axis === axis.id).map((df) => df.name),
        data: [],
      }
      if (toolkitVersion.length > 0) {
        chartData[axis.name].data = toolkitVersion.map((version) => {
          const ret = {}
          ret.date = version.modified.split('T')[0]
          version.data[axInd].domains.forEach((domain, domainInd) => {
            ret['axis' + (domainInd + 1)] = domain.domain_percentage / 100
          })
          return ret
        })
      }
      if (toolkitData.length > 0) {
        const current = { date: todayString }
        toolkitData[axInd].domains.forEach((dom, ii) => {
          current['axis' + (ii + 1)] = dom.domain_percentage / 100
        })
        chartData[axis.name].data.push(current)
      }
    })
    return chartData
  },
  getCoverageData: (state, getters) => {
    const coverageVersion = getters.getCoverageVersions
    const projectData = getters.getCurrentProject
    if (projectData) {
      const coverage = projectData.coverage ? projectData.coverage.slice() : []
      coverage.push(Object.assign({}, projectData.national_level_deployment))
      coverageVersion.push({ data: coverage })

      const todayString = getTodayString()

      return coverageVersion.reduce(
        (ret, versionObj, vInd) => {
          ret.data[vInd] = {}
          ret.data[vInd].date = versionObj.modified
            ? versionObj.modified.split('T')[0]
            : todayString

          versionObj.data.forEach((distrObj) => {
            forOwn(distrObj, (val, key) => {
              const labels = ['clients', 'facilities', 'health_workers']
              const index = labels.indexOf(key)
              if (index > -1) {
                const name = `axis${index + 1}`
                ret.data[vInd][name] = (ret.data[vInd][name] || 0) + val
              }
            })
          })
          return ret
        },
        { labels: [], data: [] }
      )
    }
  },
}

export const actions = {
  async loadUserProjects({ commit }) {
    try {
      const { data } = await this.$axios.get(
        '/api/projects/user-list/member-of/'
      )
      data.sort((a, b) => b.id - a.id)
      commit('SET_USER_PROJECT_LIST', data)
    } catch (error) {
      console.error('projects/loadUserProjects failed')
      return Promise.reject(error)
    }
  },
  async getInitiatives({ state, commit, dispatch, rootGetters }) {
    commit('SET_VALUE', { key: 'loadingProject', val: true })
    commit('SET_VALUE', { key: 'userProjects', val: [] })
    await dispatch('user/refreshProfile', {}, { root: true })
    const user = rootGetters['user/getProfile']
    try {
      const results = await Promise.all([
        this.$axios.get(`/api/projects/user-list/member-of/`),
        this.$axios.get(`/api/projects/user-list/review/`),
        this.$axios.get(`/api/projects/user-list/favorite/`),
      ])
      // for review case
      if (state.tab === 2) {
        let { data } = results[state.tab - 1]
        data.sort((a, b) => b.id - a.id)
        data = data.map((p) => {
          const project = p.project
          return {
            reviewId: p.id,
            ...p,
            ...project,
            favorite: user ? user.favorite.includes(p.project.id) : undefined,
            isMember: user ? user.member.includes(p.id) : undefined,
            isViewer: user ? user.viewer.includes(p.id) : undefined,
            isPublished: true,
          }
        })
        commit('SET_VALUE', { key: 'userProjects', val: data })
      } else {
        let { data } = results[state.tab - 1]
        data.sort((a, b) => b.id - a.id)
        data = data.map((p) => {
          const project =
            p.published && p.published.name ? p.published : p.draft
          return {
            ...p,
            ...project,
            favorite: user ? user.favorite.includes(p.id) : undefined,
            isMember: user ? user.member.includes(p.id) : undefined,
            isViewer: user ? user.viewer.includes(p.id) : undefined,
            isPublished: !!(p.published && p.published.name),
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
            total: results[0].data.length,
          },
          {
            id: 2,
            name: 'My reviews',
            icon: 'comment-alt',
            total: results[1].data.length,
          },
          {
            id: 3,
            name: 'My favorites',
            icon: 'heart',
            total: results[2].data.length,
          },
        ],
      })
      commit('SET_VALUE', { key: 'loadingProject', val: false })
    } catch (e) {
      console.log(e.response.data)
      commit('SET_VALUE', { key: 'loadingProject', val: false })
      console.error('portfolio/loadPortfolioProjects failed')
    }
  },
  async addReview({ state, commit, dispatch }, { id, ...score }) {
    try {
      commit('SET_VALUE', { key: 'loadingReview', val: true })
      await this.$axios.post(`/api/project-review/${id}/fill/`, {
        ...score,
      })
      // update initiatives
      dispatch('getInitiatives')
      // interface setters
      commit('SET_VALUE', { key: 'loadingReview', val: false })
      commit('SET_VALUE', { key: 'dialogReview', val: false })
    } catch (e) {
      console.log(e.response.data)
    }
  },
  async setCurrentProject({ commit, dispatch }, id) {
    id = parseInt(id, 10)
    try {
      await dispatch('loadProjectDetails', id)
    } catch (e) {
      console.error('projects/setCurrentProject failed')
      return Promise.reject(e)
    }
    commit('SET_CURRENT_PROJECT', id)
  },
  async loadProjectDetails({ commit, rootGetters }, projectId) {
    const profile = rootGetters['user/getProfile']
    try {
      if (projectId && profile) {
        const [toolkitVersions, coverageVersions] = await Promise.all([
          this.$axios.get(`/api/projects/${projectId}/toolkit/versions/`),
          this.$axios.get(`/api/projects/${projectId}/coverage/versions/`),
        ])
        commit('SET_CURRENT_PROJECT_TOOLKIT', toolkitVersions.data)
        commit('SET_CURRENT_PROJECT_COVERAGE_VERSIONS', coverageVersions.data)
      }
    } catch (error) {
      console.error('projects/loadProjectDetails failed')
      return Promise.reject(error)
    }
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
    // update initiatives/projects by tab click
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
          await dispatch('getInitiatives')
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

  // state interaction handlers
  setCurrentProjectReview({ commit }, val) {
    commit('SET_VALUE', { key: 'currentProjectReview', val })
  },
  setReviewDialog({ commit }, val) {
    commit('SET_VALUE', { key: 'dialogReview', val })
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
  SET_CURRENT_PROJECT_TOOLKIT: (state, toolkit) => {
    state.currentProjectToolkitVersions = toolkit
  },
  SET_CURRENT_PROJECT_COVERAGE_VERSIONS: (state, coverage) => {
    state.currentProjectCoverageVersions = coverage
  },
  RESET_PROJECTS_DATA: (state) => {
    state.userProjects = []
    state.currentProject = null
    state.projectStructure = {}
    state.currentProjectToolkitVersions = []
    state.currentProjectCoverageVersions = []
  },
}
