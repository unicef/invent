import { objectToQueryString } from '@/utilities/search'

export const state = () => ({
  filter: {
    q: '',
    portfolio: '',
    type: 'portfolio',
    portfolio_page: 'inventory',
  },
})

export const actions = {
  saveAnswer({ state, commit, dispatch, rootState }, answer) {},
  async getSearch({ state, commit, dispatch }) {
    try {
      const query = objectToQueryString(state.filter)
      const {
        data: {
          results: { projects },
        },
      } = await this.$axios.get(`api/search${query}`)
      console.log(projects)
      dispatch('portfolio/setProjects', projects, { root: true })
    } catch (e) {
      console.error('search failed')
    }
  },
  resetSearch({ commit }) {
    commit('SET_SEARCH', { key: 'q', val: '' })
  },
}
// Reducers
export const mutations = {
  SET_SEARCH(state, { key, val }) {
    console.log(key, val)
    state.filter[key] = val
  },
}
