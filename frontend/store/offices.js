export const state = () => ({
  offices: [],
  office: {},
  current: 0,
})

export const getters = {
  getOffices(state) {
    return state.offices
  },
  getOfficeDetails: (state) => (id) => {
    const office = state.offices.find((o) => o.id === id)
    return office || undefined
  },
}

export const mutations = {
  SET_OFFICES: (state, arr) => {
    state.offices = arr
  },
  SET_OFFICE: (state, obj) => {
    state.office = obj
  },
  SET_CURRENT: (state, id) => {
    state.current = id
  },
}

export const actions = {
  async loadOffices({ state, commit }) {
    if (state.offices.length > 0) return
    const data = await utilities.handleRequest(this.$axios)
    utilities.sortArr(data instanceof Error ? [] : data)
    commit('SET_OFFICES', data instanceof Error ? [] : data)
  },
  async loadOffice({ commit }, id = 1) {
    const data = await utilities.handleRequest(this.$axios, id)
    commit('SET_OFFICE', data instanceof Error ? {} : data)
  },
  setOffice({ commit }, id) {
    commit('SET_CURRENT', id)
  },
}

const utilities = {
  sortArr(data) {
    return data.sort((a, b) => a.name.localeCompare(b.name))
  },
  async handleRequest(axios, id = '') {
    try {
      const { data } = await axios.get(`/api/countryoffices/${id}`)
      return data
    } catch (e) {
      console.error(`/api/countryoffices/${id} failed`)
      return e
    }
  },
}
