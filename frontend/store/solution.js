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
})

export const state = () => ({
  ...cleanState(),
})

export const getters = {
  getSolutionData: (state) => ({
    ...state,
  }),
  getPortfoliosList: (state) => state.portfolio_list,
  getProblemStatementList: (state) => state.problem_statement_list,
}

export const actions = {
  async loadSolution({ commit }, id) {
    return this.$axios.get(`/api/solutions/${id}`).then((response) => {
      commit('PUT_SOLUTION', response.data)
    })
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
  async setSolution({ commit }, data) {
    return this.$axios.put(`api/solutions/${id}`)
  },
  async deleteSolution({ state }) {
    return this.$axios({
      method: 'put',
      url: `api/solutions/${state.id}`,
      data: { ...state, isActive: false },
    })
  },
}

export const mutations = {
  PUT_SOLUTION: (state, data) => {
    state.id = data.id
    state.name = data.name
    state.phase = data.phase
    state.open_source_frontier_tech = data.open_source_frontier_tech ? 'Yes' : 'No'
    state.learning_investment = data.learning_investment ? 'Yes' : 'No'
    state.people_reached = data.people_reached
    state.portfolios = data.portfolios
    state.portfolio_problem_statements = data.portfolio_problem_statements
  },
  PUT_PROBLEM_STATEMENTS_LIST: (state, data) => {
    state.problem_statement_list = data
  },
  PUT_PORTFOLIO_LIST: (state, data) => {
    state.portfolio_list = data
  },
}
