import { objectToQueryString, queryStringToObject } from '@/utilities/search'

export const state = () => ({
  tabs: false,
  currentFilter: undefined,
  filters: {},
  tabsSearchKeys: {
    q: '',
    // in: ['name', 'org', 'country', 'overview', 'loc'],
    country: [], // array
    sw: [],
    dhi: [],
    hfa: [],
    hsc: [],
    region: '',
    // partner: [],
    co: [], // array
    goal: '',
    result: '',
    cl: [],
    cc: [],
    cs: [],
    ic: [], // array
    sp: '',
    ps: '',
  },
  loading: false,
})

export const actions = {
  async getFilters({ state, commit, dispatch, rootState }) {
    try {
      const {
        data: { filters },
      } = await this.$axios.get(
        `/api/userprofiles/${rootState.user.profile.id}/`
      )
      commit('SET_VALUE', { key: 'filters', val: filters })
    } catch (e) {
      console.error('get filters failed')
    }
  },
  setCurrentFilter({ state, commit, dispatch }, val = undefined) {
    commit('SET_VALUE', { key: 'currentFilter', val })
  },
  async setFilters({ state, commit, dispatch }, name) {
    await dispatch('resetFilters')
    commit('SET_VALUE', { key: 'currentFilter', val: name })
    if (state.tabs) {
      const newFilters = queryStringToObject(state.filters[name])
      dispatch('dashboard/setSearchOptions', newFilters, {
        root: true,
      })
      for (const key in state.tabsSearchKeys) {
        if (newFilters[key] !== undefined) {
          const filter = newFilters[key]
          let val =
            Array.isArray(filter) || !/\d/.test(filter)
              ? filter
              : ['country', 'co', 'ic'].includes(key)
              ? [parseInt(filter)]
              : parseInt(filter)
          val = ['country', 'co', 'ic'].includes(key)
            ? val.map((i) => parseInt(i))
            : val
          await commit('search/SET_SEARCH', { key, val }, { root: true })
        }
      }
      await dispatch('search/getSearch', {}, { root: true })
    } else {
      dispatch(
        'dashboard/setSearchOptions',
        queryStringToObject(state.filters[name]),
        {
          root: true,
        }
      )
    }
  },
  async newFilter({ commit, state, dispatch, rootState, rootGetters }, name) {
    commit('SET_VALUE', { key: 'loading', val: true })
    const newFilter = {
      [name]: state.tabs
        ? objectToQueryString(rootState.search.filter)
        : objectToQueryString(rootGetters['dashboard/getSearchParameters']),
    }
    await dispatch('updateFilter', {
      ...state.filters,
      ...newFilter,
    })
    await dispatch('setFilters', name)
    commit('SET_VALUE', { key: 'loading', val: false })
  },
  async deleteFilter({ state, dispatch }, name = '') {
    const filters = state.filters
    delete filters[name]
    await dispatch('updateFilter', filters)
    if (name === state.currentFilter) {
      await dispatch('setFilters', undefined)
    }
  },
  async updateFilter({ state, commit, dispatch, rootState }, updateFilters) {
    try {
      const {
        data: { filters },
      } = await this.$axios.patch(
        `/api/userprofiles/${rootState.user.profile.id}/`,
        {
          filters: updateFilters,
        }
      )
      commit('SET_VALUE', { key: 'filters', val: filters })
    } catch (e) {
      console.error('update filter failed')
    }
  },
  resetFilters({ state, commit, dispatch }) {
    if (state.tabs) {
      dispatch('search/resetSearch', {}, { root: true })
    } else {
      dispatch('dashboard/resetUserInput', {}, { root: true })
    }
  },
}
export const mutations = {
  SET_VALUE(state, { key, val }) {
    state[key] = val
  },
}
