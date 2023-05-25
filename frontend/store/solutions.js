const cleanState = () => ({
  allSolutionsList: {},
  allActiveSolutionsList: [],
})

export const state = () => ({
  ...cleanState(),
})

export const getters = {
  getSolutionsList: (state, getters, rootState, rootGetters) => {
    const phases = rootGetters['system/getSolutionPhases']
    const solWithPhases = state.allSolutionsList.solutions.map((solution) => {
      const phaseName = phases.find((phase) => phase.id === solution.phase).name
      return { ...solution, phase_name: phaseName }
    })
    return solWithPhases
  },
  getAllActiveSolutionsList: (state, getters, rootState, rootGetters) => {
    const phases = rootGetters['system/getSolutionPhases']
    const solWithPhases = state.allActiveSolutionsList.map((solution) => {
      const phaseName = phases.find((phase) => phase.id === solution.phase).name
      return { ...solution, phase_name: phaseName }
    })
    return solWithPhases
  },
}

export const actions = {
  async loadSolutionsList({ state, commit, dispatch, rootGetters }, id) {
    const response = await this.$axios.get(`/api/portfolio/${id}`)
    commit('PUT_SOLUTION_LIST', response.data)
  },
  async loadAllActiveSolutionsList({ commit }) {
    const response = await this.$axios.get('api/solution')
    commit('PUT_ALL_ACTIVE_SOLUTIONS_LIST', response.data)
  },
}

export const mutations = {
  PUT_SOLUTION_LIST: (state, data) => {
    state.allSolutionsList = data
  },
  PUT_ALL_ACTIVE_SOLUTIONS_LIST: (state, data) => {
    state.allActiveSolutionsList = data
  },
}
