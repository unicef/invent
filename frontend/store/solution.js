const cleanState = () => ({
  id: '',
  name: '',
  phase: '',
  open_source_frontier_tech: '',
  learning_investment: '',
  portfolios: [],
  people_reached: '',
  countries: [],
  problem_statements: [],
})

export const state = () => ({
  ...cleanState(),
})

export const getters = {
  getSolutionData: (state) => ({
    ...state,
  }),
}

export const actions = {
  async loadSolution({ commit }, id) {
    return this.$axios.get(`/api/solutions/${id}`).then((response) => {
      commit('PUT_SOLUTION', response.data)
    })
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
  },
}
