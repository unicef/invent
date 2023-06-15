import { stateGenerator, gettersGenerator, actionsGenerator, mutationsGenerator } from '../utilities/map'

export const state = () => ({
  ...stateGenerator(),
  landingPageData: null,
  searched: null,
  foundIn: {},
  newsFeed: [],
  countryProjectsList: [],
})

export const getters = {
  ...gettersGenerator(),
  getCountryProjectsList: (state) => state.countryProjectsList,
  getSearched: (state) => state.searched,
  getNewsFeed: (state) => state.newsFeed,
  getLandingPageData: (state) => state.landingPageData,
  getSearchResult: (state, getters) => {
    if (state.searched && state.searched === state.searchString) {
      return getters.getProjectsMap
    }
    return []
  },
  getFoundIn: (state) => (id) => {
    const result = []
    for (const category in state.foundIn) {
      if (state.foundIn[category].includes(id)) {
        result.push(category)
      }
    }
    return result
  },
}

export const actions = {
  ...actionsGenerator(),
  async loadCountryProjectsList({ commit, getters }) {
    const countryId = getters.getLandingPageData.id

    if (countryId) {
      try {
        const response = await this.$axios.get(`/api/search/?type=list&country=${countryId}&page_size=999999`)

        commit('SET_COUNTRY_PROJECTS_LIST', response.data.results.projects)
      } catch (e) {
        console.log(e)
      }
    }
  },
  async search({ commit, dispatch }) {
    try {
      commit('SET_SEARCHED', null)
      const { results } = await dispatch('loadProjects')
      commit('SET_PROJECT_MAP', results.projects)
      commit('SET_SEARCHED', results.search_term)
      commit('SET_FOUND_IN', results.found_in)
    } catch (e) {
      // console.log(e);
    }
  },
  async loadCustomLandingPage({ dispatch }, code) {
    if (code.length === 2) {
      await dispatch('loadCountryData', code)
    } else if (code.length > 2) {
      await dispatch('loadDonorData', code)
    }
  },
  async loadNewsFeed({ commit }) {
    try {
      const { data } = await this.$axios.get(`/api/news-feed/`)
      commit('SET_VALUE', { key: 'newsFeed', val: data })
    } catch (e) {
      console.error('landing/loadNewsFeed failed')
    }
  },
  async loadCountryData({ commit, dispatch, rootGetters }, code) {
    try {
      const country = rootGetters['countries/getCountries'].find((c) => c.code.toLowerCase() === code.toLowerCase())
      const { data } = await this.$axios.get(`/api/landing-country/${country.id}/`)
      await dispatch('setSelectedCountry', data.id)
      commit('SET_LANDING_PAGE_DATA', Object.freeze(data))
    } catch (e) {
      console.error('landing/loadCountryData failed')
    }
  },
  async loadDonorData({ commit, rootGetters }, code) {
    try {
      const donor = rootGetters['system/getDonors'].find((d) => d.code.toLowerCase() === code.toLowerCase())
      const { data } = await this.$axios.get(`/api/landing-donor/${donor.id}/`)
      commit('SET_LANDING_PAGE_DATA', Object.freeze(data))
    } catch (e) {
      console.error('landing/loadDonorData failed')
    }
  },
  clearCustomLandingPage({ commit }) {
    commit('SET_LANDING_PAGE_DATA', null)
  },
  resetSearch({ commit }) {
    commit('SET_SEARCHED', null)
    commit('SET_SEARCH_STRING', null)
  },
}
export const mutations = {
  ...mutationsGenerator(),
  SET_VALUE(state, { key, val }) {
    state[key] = val
  },
  SET_LANDING_PAGE_DATA: (state, data) => {
    state.landingPageData = data
  },
  SET_SEARCHED: (state, searched) => {
    state.searched = searched
  },
  SET_FOUND_IN: (state, found) => {
    state.foundIn = { ...found }
  },
  SET_COUNTRY_PROJECTS_LIST: (state, data) => {
    state.countryProjectsList = data
  },
}
