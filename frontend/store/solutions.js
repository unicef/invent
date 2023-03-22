const cleanState = () => ({})

export const state = () => ({
  ...cleanState(),
})

export const getters = {}

export const actions = {
  async loadSolution({ state, commit, dispatch, rootGetters }, id) {
    const data = await this.$axios.get(`/api/solutions/`)
    console.log(data)
  },
}

export const mutations = {}
