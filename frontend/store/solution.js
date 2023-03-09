const cleanState = () => ({
  id: '',
  name: '',
  phase: '',
  open_source_frontier_tech: '',
  learning_investment: '',
  portfolios: [],
  people_reached: '',
  problem_statements: [],
  country_solutions: [],
  problem_statement_list: [],
  portfolio_list: [],
})

export const state = () => ({
  ...cleanState(),
})

export const getters = {
  getSolutionData: (state) => ({
    ...state,
  }),
  getPorfoliosList: (state) => state.portfolio_list,
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
}

export const mutations = {
  PUT_SOLUTION: (state, data) => {
    state.id = data.id
    state.name = data.name
    state.phase = data.phase
    state.open_source_frontier_tech = data.open_source_frontier_tech ? 'Yes' : 'No'
    state.learning_investment = data.learning_investment ? 'Yes' : 'No'
    state.people_reached = data.people_reached
    state.country_solutions = data.country_solutions
    state.portfolios = data.portfolios
    state.problem_statements = data.problem_statements
  },
  PUT_PROBLEM_STATEMENTS_LIST: (state, data) => {
    state.problem_statement_list = data
  },
  PUT_PORTFOLIO_LIST: (state, data) => {
    state.portfolio_list = data
  },
}
