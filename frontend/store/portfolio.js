import { toInteger } from 'lodash'
import filter from 'lodash/filter'

export const state = () => ({
  loading: false,
  name: '',
  projectName: '',
  description: '',
  status: 'DR',
  icon: null,
  managers: [],
  statements: [],
  // portfolio icon set metadata
  icons: [
    { id: '1', title: 'education', icon: 'education' },
    { id: '2', title: 'nutrition', icon: 'nutrition' },
    { id: '3', title: 'health', icon: 'health' },
    { id: '4', title: 'child_protection', icon: 'child_protection' },
    { id: '5', title: 'wash', icon: 'wash' },
    { id: '6', title: 'aids', icon: 'aids' },
    { id: '7', title: 'social_inclusion', icon: 'social_inclusion' },
    { id: '8', title: 'food_health', icon: 'food_health' },
    { id: '9', title: 'affected_population', icon: 'affected_population' },
    { id: '10', title: 'children', icon: 'children' },
    { id: '11', title: 'gender_balance', icon: 'gender_balance' },
    { id: '14', title: 'infant', icon: 'infant' },
    { id: '15', title: 'breast_feeding', icon: 'breast_feeding' },
    {
      id: '16',
      title: 'children_with_disabilities',
      icon: 'children_with_disabilities',
    },
    { id: '27', title: 'pregnant', icon: 'pregnant' },
    { id: '29', title: 'mental_health', icon: 'mental_health' },
    { id: '30', title: 'mother_and_baby', icon: 'mother_and_baby' },
    { id: '34', title: '5year_old_girl', icon: '5year_old_girl' },
    { id: '38', title: 'conflict', icon: 'conflict' },
    { id: '42', title: 'tsunami', icon: 'tsunami' },
    { id: '45', title: 'epidemic', icon: 'epidemic' },
    { id: '52', title: 'tent', icon: 'tent' },
    { id: '69', title: 'medical_supplies', icon: 'medical_supplies' },
    { id: '70', title: 'vaccines', icon: 'vaccines' },
    { id: '71', title: 'psychosocial_support', icon: 'psychosocial_support' },
    { id: '72', title: 'headquarters', icon: 'headquarters' },
    { id: '73', title: 'regional_office', icon: 'regional_office' },
    { id: '92', title: 'partnership', icon: 'partnership' },
    { id: '97', title: 'advocacy', icon: 'advocacy' },
    { id: '113', title: 'innovation', icon: 'innovation' },
    { id: '116', title: 'community_building', icon: 'community_building' },
    { id: '164', title: 'emergency', icon: 'emergency' },
  ],
  statusList: [
    { id: 'ACT', name: 'Active' },
    { id: 'DR', name: 'Draft' },
    { id: 'ARC', name: 'Archived' },
  ],
  portfolios: [],
  portfolio: {},
  projects: [],
  // review and score
  review: {},
  problemStatements: [],
  loadingScore: false,
  // add reviewer
  loadingAddReviewers: false,
  // dashboard of portfolio manager interactions
  tabs: [
    {
      id: 1,
      name: 'Inventory',
      icon: 'folder',
      total: 1,
      portfolio_page: 'inventory',
    },
    {
      id: 2,
      name: 'For review',
      icon: 'eye',
      total: 1,
      portfolio_page: 'review',
    },
    {
      id: 3,
      name: 'Portfolio',
      icon: 'briefcase',
      total: 1,
      portfolio_page: 'portfolio',
    },
  ],
  tab: 1,
  dialogReview: false,
  dialogScore: false,
  dialogError: false,
  currentProjectId: null,
  currentPortfolioId: null,
  // tooltip display on actions
  back: 0,
  forward: 1,
  // error handling
  // dialogError: false,
  errorMessage: '',
  // question type
  questionType: [
    'psa',
    'rnci',
    'ratp',
    'ra',
    'ee',
    'nst',
    'nc',
    'ps',
    'impact',
    'scale_phase',
  ],
  // pagination
  total: 0,
})

export const getters = {
  getName: (state) => state.name,
  getDescription: (state) => state.description,
  getStatus: (state) => state.status,
  getIcon: (state) => state.icon,
  getManagers: (state) => state.managers,
  getStatements: (state) => state.statements,
  getLoading: (state) => state.loading,
  getPortfolios: (state) => state.portfolios,
  getActivePortfolios: (state) => {
    return filter(
      state.portfolios,
      (portfolio) => portfolio.status === 'active'
    )
  },
}

export const actions = {
  setName({ commit }, value) {
    commit('SET_NAME', value)
  },
  setDescription({ commit }, value) {
    commit('SET_DESCRIPTION', value)
  },
  setStatus({ commit }, value) {
    commit('SET_STATUS', value)
  },
  setIcon({ commit }, value) {
    commit('SET_ICON', value)
  },
  setManagers({ commit }, value) {
    commit('SET_MANAGERS', value)
  },
  setStatements({ commit }, value) {
    commit('SET_STATEMENTS', value)
  },
  setLoading({ commit }, value) {
    commit('SET_LOADING', value)
  },
  setTab({ state, commit, dispatch }, val) {
    commit('SET_TAB', val)
    commit('SET_VALUE', { key: 'back', val: state.tab - 2 })
    commit('SET_VALUE', { key: 'forward', val: state.tab })
    commit(
      'search/SET_SEARCH',
      {
        key: 'portfolio_page',
        val: state.tabs.find((i) => i.id === val).portfolio_page,
      },
      { root: true }
    )
    // update portfolio
    dispatch('getPortfolioProjects')
    // reset on tab change the status selection
    dispatch('dashboard/setSelectedRows', [], { root: true })
    dispatch('search/resetSearch', [], { root: true })
  },
  // portfolio actions
  async createPortfolio({ state, getters, dispatch }) {
    dispatch('setLoading', 'create')
    await this.$axios.post(`/api/portfolio/create/`, {
      name: state.name,
      description: state.description,
      status: state.status,
      icon: state.icon.id,
      managers: state.managers,
      problem_statements: state.statements.filter((i) => i.name !== ''),
    })
    dispatch('setLoading', false)
  },
  async editPortfolio({ state, getters, dispatch }, id) {
    dispatch('setLoading', 'edit')
    await this.$axios.patch(`/api/portfolio/update/${id}/`, {
      name: state.name,
      description: state.description,
      status: state.status,
      icon: state.icon.id,
      managers: state.managers,
      problem_statements: state.statements.filter((i) => i.name !== ''),
    })
    dispatch('setLoading', false)
  },
  async getPortfolios({ state, commit, dispatch }) {
    const { data } = await this.$axios.get('api/portfolio/manager-of/')
    const portfolios = data.map((i) => {
      const icon = state.icons.find((item) => item.id === i.icon).icon
      return {
        id: i.id,
        name: i.name,
        total: i.project_count,
        status: status(i.status),
        description: i.description,
        ps: i.problem_statements,
        icon,
      }
    })
    commit('SET_VALUE', { key: 'portfolios', val: portfolios })
  },
  async getPortfolioDetails({ state, commit, dispatch }, id) {
    const { data } = await this.$axios.get(`api/portfolio/manager-of/`)
    const {
      name,
      description,
      status,
      icon,
      managers,
      problem_statements,
    } = data.find((i) => i.id === toInteger(id, 10))

    commit('SET_VALUE', { key: 'name', val: name })
    commit('SET_VALUE', { key: 'description', val: description })
    commit('SET_VALUE', { key: 'status', val: status })
    commit('SET_VALUE', {
      key: 'icon',
      val: state.icons.find((item) => item.id === icon),
    })
    commit('SET_VALUE', { key: 'managers', val: managers })
    commit('SET_VALUE', {
      key: 'problemStatements',
      val: problem_statements,
    })
  },
  async getPortfolioProjects({ state, commit, dispatch }) {
    try {
      dispatch('getPortfolioDetails', state.currentPortfolioId)
      const baseUrl = `api/search?portfolio=${state.currentPortfolioId}&type=portfolio&portfolio_page=`
      const results = await Promise.all([
        this.$axios.get(`${baseUrl}inventory`),
        this.$axios.get(`${baseUrl}review`),
        this.$axios.get(`${baseUrl}portfolio`),
      ])
      const {
        data: {
          count,
          results: { projects },
        },
      } = results[state.tab - 1]
      // set the projects of the portfolio by tab filter
      dispatch('setProjects', { projects, count })
      // update tab counts
      commit('SET_VALUE', {
        key: 'tabs',
        val: [
          {
            id: 1,
            name: 'Inventory',
            icon: 'folder',
            total: results[0].data.count,
            portfolio_page: 'inventory',
          },
          {
            id: 2,
            name: 'For review',
            icon: 'eye',
            total: results[1].data.count,
            portfolio_page: 'review',
          },
          {
            id: 3,
            name: 'Portfolio',
            icon: 'briefcase',
            total: results[2].data.count,
            portfolio_page: 'portfolio',
          },
        ],
      })
    } catch (e) {
      // console.log(e.response.data);
      console.error('portfolio/getPortfolioProjects failed')
    }
  },
  setProjects({ state, commit, dispatch }, { projects, count }) {
    // pagination
    commit('SET_VALUE', { key: 'total', val: count })
    // projects
    commit('SET_VALUE', {
      key: 'projects',
      val: projects.map((i) => {
        // todo: set this attributes from api
        return {
          ...i,
          favorite: Math.random() >= 0.5,
          ...i.project_data,
        }
      }),
    })
  },
  // move action
  async moveToState({ state, commit, dispatch }, { type, project, tab }) {
    // add-project, remove-project, approve-project, disapprove-project
    try {
      await this.$axios.post(
        `/api/portfolio/${state.currentPortfolioId}/${type}/`,
        { project }
      )
      dispatch('setTab', tab)
    } catch (e) {
      commit('SET_VALUE', {
        key: 'errorMessage',
        val: e.response.data.project,
      })
      commit('SET_VALUE', { key: 'dialogError', val: true })
    }
  },
  // review actions
  async addReview({ state, commit, dispatch }, { id, message, reviewers }) {
    try {
      commit('SET_VALUE', { key: 'loadingAddReviewers', val: true })
      await this.$axios.post(
        `/api/portfolio/${state.currentPortfolioId}/${id}/`,
        {
          userprofile: reviewers,
          message,
        }
      )
      // update portfolio
      dispatch('getPortfolioProjects')
      // interface setters
      commit('SET_VALUE', { key: 'loadingAddReviewers', val: false })
      commit('SET_VALUE', { key: 'dialogReview', val: false })
    } catch (e) {
      console.log(e.response.data)
    }
  },
  // score actions
  async addScore({ state, commit, dispatch }, { id, data }) {
    try {
      // fix from elemnt ui "" default setup
      const officialScore = {}
      for (const [key, value] of Object.entries(data)) {
        officialScore[key] = value === '' ? null : value
      }
      commit('SET_VALUE', { key: 'loadingScore', val: true })
      await this.$axios.post(`/api/project-review/manager/${id}/`, {
        ...officialScore,
      })
      // update portfolio
      dispatch('getPortfolioProjects')
      // interface setters
      commit('SET_VALUE', { key: 'loadingScore', val: false })
      commit('SET_VALUE', { key: 'dialogScore', val: false })
    } catch (e) {
      console.log(e.response.data)
    }
  },
  async getManagerScore({ state, commit, dispatch }, { id, name }) {
    try {
      const { data } = await this.$axios.get(
        `api/project-review/manager/${id}/`
      )
      commit('SET_VALUE', { key: 'projectName', val: name })
      commit('SET_VALUE', {
        key: 'review',
        val: { ...data },
      })
      commit('SET_VALUE', { key: 'dialogScore', val: true })
    } catch (e) {
      console.log(e.response.data)
    }
  },
  // state interaction handlers
  setCurrentProjectId({ commit }, val) {
    commit('SET_VALUE', { key: 'currentProjectId', val })
  },
  setReviewDialog({ commit }, val) {
    commit('SET_VALUE', { key: 'dialogReview', val })
  },
  setScoreDialog({ commit }, val) {
    commit('SET_VALUE', { key: 'dialogScore', val })
  },
  setErrorDialog({ commit }, val) {
    commit('SET_VALUE', { key: 'dialogError', val })
  },
  resetPortfolio({ commit }) {
    commit('SET_VALUE', { key: 'name', val: '' })
    commit('SET_VALUE', { key: 'description', val: '' })
    commit('SET_VALUE', { key: 'status', val: 'DR' })
    commit('SET_VALUE', { key: 'icon', val: null })
    commit('SET_VALUE', { key: 'managers', val: [] })
    commit('SET_VALUE', { key: 'statements', val: [] })
  },
  // general pre portfolio setup
  // todo: change to portfolios API
}

export const mutations = {
  SET_VALUE(state, { key, val }) {
    state[key] = val
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_DESCRIPTION: (state, description) => {
    state.description = description
  },
  SET_STATUS: (state, status) => {
    state.status = status
  },
  SET_ICON: (state, icon) => {
    state.icon = icon
  },
  SET_MANAGERS: (state, managers) => {
    state.managers = managers
  },
  SET_STATEMENTS: (state, statements) => {
    state.statements = statements
  },
  SET_LOADING: (state, loading) => {
    state.loading = loading
  },
  SET_PORTFOLIO: (state, portfolio) => {
    state.portfolio = portfolio
  },
  SET_TAB: (state, tab) => {
    state.tab = tab
  },
}

const status = (status) => {
  switch (status) {
    case 'ACT':
      return 'active'
    case 'DR':
      return 'draft'
    case 'ARC':
      return 'archived'
    default:
      break
  }
}
