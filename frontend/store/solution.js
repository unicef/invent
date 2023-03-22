import { uuidv4 } from '~/utilities/dom'
const cleanState = () => ({
  id: '',
  isActive: true,
  created: '',
  modified: '',
  name: '',
  phase: 0,
  open_source_frontier_tech: false,
  learning_investment: false,
  portfolios: [],
  people_reached: 0,
  problem_statements: [],
  country_solutions: [],
  problem_statement_list: [],
  portfolio_list: [],
  portfolio_problem_statements: [],
  loading: false,
})

export const state = () => ({
  ...cleanState(),
})

export const getters = {
  getSolutionData: (state) => ({
    ...state,
  }),
  getLoading: (state) => state.loading,
  getPortfoliosList: (state) => state.portfolio_list,
  getProblemStatementList: (state) => state.problem_statement_list,
}

export const actions = {
  async loadSolution({ commit }, id) {
    return this.$axios.get(`/api/solutions/${id}`).then((response) => {
      commit('LOAD_SOLUTION', response.data)
    })
  },
  setLoading({ commit }, loadingState) {
    commit('SET_LOADING', loadingState)
  },
  async loadProblemPortfoliolists({ state, commit }) {
    if (!state.problem_statement_list.length > 0) {
      this.$axios
        .get('/api/problem-statement/')
        .then((response) => commit('PUT_PROBLEM_STATEMENTS_LIST', response.data))
    }
    if (!state.portfolio_list.length > 0) {
      this.$axios.get('/api/portfolio/active-list/').then((response) => commit('PUT_PORTFOLIO_LIST', response.data))
    }
  },
  async updateSolution({ state }, data) {
    return this.$axios({
      method: 'put',
      url: `/api/solution/update/${state.id}/`,
      data: {
        name: data.name,
        is_active: true,
        phase: data.phase,
        open_source_frontier_tech: data.open_source_frontier_tech,
        learning_investment: data.learning_investment,
        people_reached: data.people_reached,
        country_solutions: data.country_solutions,
        portfolio_problem_statements: data.portfolio_problem_statements,
      },
    })
  },
  async deleteSolution({ state }) {
    return this.$axios({
      method: 'put',
      url: `/api/solution/update/${state.id}/`,
      data: {
        name: state.name,
        is_active: false,
        phase: state.phase,
        open_source_frontier_tech: state.open_source_frontier_tech,
        learning_investment: state.learning_investment,
        people_reached: state.people_reached,
        country_solutions: state.country_solutions,
        portfolio_problem_statements: state.portfolio_problem_statements,
      },
    })
  },
  cancelSolution({ commit }) {
    commit('INIT_STATE')
  },
}

export const mutations = {
  LOAD_SOLUTION: (state, data) => {
    state.id = data.id
    state.name = data.name
    state.phase = data.phase
    state.open_source_frontier_tech = data.open_source_frontier_tech
    state.learning_investment = data.learning_investment
    state.people_reached = data.people_reached
    state.portfolios = data.portfolios
    state.country_solutions = data.country_solutions.map((sol) => ({ ...sol, row_id: uuidv4() }))
    state.portfolio_problem_statements = data.portfolio_problem_statements
  },
  PUT_PROBLEM_STATEMENTS_LIST: (state, data) => {
    state.problem_statement_list = data
  },
  PUT_PORTFOLIO_LIST: (state, data) => {
    state.portfolio_list = data
  },
  INIT_STATE: (state) => {
    state = cleanState()
  },
  SET_LOADING: (state, loadingState) => {
    state.loading = loadingState
  },
}
