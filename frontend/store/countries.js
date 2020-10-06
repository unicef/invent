import uniqBy from 'lodash/uniqBy'

export const state = () => ({
  countries: [],
  geoJsonLibrary: {},
  countryLibrary: {},
})
export const getters = {
  getCountries(state) {
    return [...state.countries.map((c) => ({ ...c }))]
  },
  getGeoJsonLibrary(state) {
    return state.geoJsonLibrary
  },
  getCountryDetails: (state, getters) => (id) => {
    const country = {
      ...getters.getCountries.find((c) => c.id === id),
      ...state.countryLibrary[id],
    }
    return {
      ...country,
      geoJson: getters.getCountryGeoJson(id),
      districts: getters.getCountryFirstSubLevel(id),
    }
  },
  getCountryGeoJson: (state, getters) => (id) => {
    return getters.getGeoJsonLibrary[id]
  },
  getCountrySubLevelNames: (state, getters, rootState, rootGetters) => (id) => {
    const c = getters.getCountryDetails(id)
    const types = rootGetters['system/getSubLevelTypes']
    try {
      let first = types.find((t) => t.name === c.map_data.first_sub_level.name)
      let second = types.find(
        (t) => t.name === c.map_data.second_sub_level.name
      )
      first = first ? first.displayName : c.map_data.first_sub_level.name
      second = second ? second.displayName : c.map_data.second_sub_level.name
      return { first, second }
    } catch (e) {
      return {}
    }
  },
  getCountryFirstSubLevel: (state, getters) => (id) => {
    const ln = 'en'
    const country = state.countryLibrary[id]
    if (country && country.map_data && country.map_data.first_sub_level) {
      const mapped = country.map_data.first_sub_level.elements.map((ccd) => ({
        id: ccd.id || ccd.name,
        name: ccd[`name:${ln}`] || ccd['name:en'] || ccd.name,
      }))
      return uniqBy(mapped, 'id')
    }
    return []
  },
  getCountrySecondSubLevel: (state, getters) => (id) => {
    const ln = 'en'
    const country = state.countryLibrary[id]
    if (country && country.map_data && country.map_data.second_sub_level) {
      const mapped = country.map_data.second_sub_level.elements.map((ccd) => ({
        id: ccd.id || ccd.name,
        name: ccd[`name:${ln}`] || ccd['name:en'] || ccd.name,
      }))
      return uniqBy(mapped, 'id')
    }
    return []
  },
  getCountryFacilityList: (state, getters) => (id) => {
    const country = getters.getCountries.find((c) => c.id === id)
    if (country && country.map_data && country.map_data.facilities) {
      return country.map_data.facilities
    }
    return []
  },
  getSubLevelDetails: (state) => (id) => {
    const allSubLevels = []
    for (const id in state.countryLibrary) {
      const c = state.countryLibrary[id]
      if (c && c.map_data && c.map_data.first_sub_level) {
        allSubLevels.push(...c.map_data.first_sub_level.elements)
      }
    }
    return { ...allSubLevels.find((sb) => sb.id === id) }
  },
  getCountriesByUnicefRegion: (state) => (unicefRegion) => {
    const filtered = state.countries.filter((country) => {
      return country.unicef_region === unicefRegion
    })
    return [...filtered.map((c) => ({ ...c }))]
  },
}

export const actions = {
  async loadMapData({ commit, state }) {
    if (state.countries.length === 0) {
      try {
        const { data } = await this.$axios.get('/api/landing-country/')
        data.sort((a, b) => a.name.localeCompare(b.name))
        commit('SET_COUNTRY_LIST', data)
      } catch (e) {
        console.error('countries/loadMapData failed')
      }
    }
  },
  async loadCountryDetails({ commit, state }, id) {
    if (id && !state.countryLibrary[id]) {
      try {
        const { data } = await this.$axios.get(`/api/landing-country/${id}/`)
        commit('SET_COUNTRY_DETAILS', { data, id })
      } catch (e) {
        console.error('countries/loadCountryDetails failed')
      }
    }
  },
  async loadGeoJSON({ commit, getters }, id) {
    if (!getters.getGeoJsonLibrary[id]) {
      try {
        const country = getters.getCountries.find((c) => c.id === id)
        const { data } = await this.$axios.get(
          `/static/country-geodata/${country.code.toLowerCase()}.json?version=${
            country.map_version
          }`
        )
        Object.freeze(data)
        commit('UPDATE_JSON_LIBRARY', { id, data })
      } catch (e) {
        console.error('countries/loadGeoJSON  failed')
      }
    }
  },
}

export const mutations = {
  SET_COUNTRY_LIST: (state, list) => {
    state.countries = list
  },
  SET_COUNTRY_DETAILS: (state, { data, id }) => {
    state.countryLibrary = { ...state.countryLibrary, [id]: data }
  },
  UPDATE_JSON_LIBRARY: (state, { id, data }) => {
    state.geoJsonLibrary[id] = data
  },
}
