export const state = () => ({
  list: [],
  currentElement: null,
})

export const getters = {
  getList: (state) => state.list,
  getCurrentElement: (state) => state.currentElement,
  getCurrentElementDetails: (state) =>
    state.list.find((i) => i.id === state.currentElement),
}

export const actions = {
  async loadList({ commit, rootGetters }) {
    try {
      const country = rootGetters['admin/country/getData']
      if (country) {
        const { data } = await this.$axios.get(`/api/approvals/${country.id}/`)
        commit('SET_LIST', data)
      }
    } catch (e) {
      console.error('approval list failed to load', e)
    }
  },
  setCurrentElement({ commit }, value) {
    commit('SET_CURRENT_ELEMENT', value)
  },
  async updateProjectApproval({ commit, getters }, form) {
    const id = getters.getCurrentElement
    const { data } = await this.$axios.put(`/api/approval/${id}/`, form)
    commit('UPDATE_ENTRY', data)
  },
}

export const mutations = {
  SET_LIST: (state, list) => {
    state.list = list
  },
  UPDATE_ENTRY: (state, entry) => {
    const index = state.list.findIndex((i) => i.id === entry.id)
    state.list.splice(index, 1, entry)
  },
  SET_CURRENT_ELEMENT: (state, currentElement) => {
    state.currentElement = currentElement
  },
}
