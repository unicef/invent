export const state = () => ({
  geoJson: null,
  countryCenter: null,
  secondSubLevelSource: null,
  firstSubLevel: '',
  firstSubLevelType: null,
  firstSubLevelList: [],
  secondSubLevel: '',
  secondSubLevelType: null,
  secondSubLevelList: [],
  facilities: [],
  subLevelsPolyCenters: [],
})

export const getters = {
  getGeoJson(state) {
    return state.geoJson
  },
  getCountryBorder(state, getters) {
    const geoJson = getters.getGeoJson
    if (geoJson && geoJson.features && geoJson.features.length > 0) {
      return geoJson.features.find((f) => f.properties.admin_level === '2')
    }
  },
  getSecondSubLevelSource(state) {
    return state.secondSubLevelSource
  },
  getSubLevelFeatures(state, getters) {
    const geoJson = getters.getGeoJson
    let result = []
    if (geoJson && geoJson.features && geoJson.features.length > 0) {
      result = geoJson.features.filter((f) => f.properties.admin_level !== '2')
    }
    if (geoJson && geoJson.features && result.length === 0) {
      result = geoJson.features.filter((f) => f.properties.admin_level === '2')
    }
    return result.map((r) => JSON.parse(JSON.stringify(r)))
  },
  getSubLevels(state, getters) {
    const features = getters.getSubLevelFeatures
    const levels = []
    if (features) {
      for (const f of features) {
        if (!levels.includes(f.properties.admin_level)) {
          levels.push(f.properties.admin_level)
        }
      }
    }
    return levels
  },
  getSubLevelsPolyCenters(state) {
    return [
      ...state.firstSubLevelList
        .filter((p) => p.polyCenter)
        .map((pc) => ({ ...pc, polyCenter: { ...pc.polyCenter } })),
    ]
  },
  getFirstSubLevelMap(state, getters) {
    const features = getters.getSubLevelFeatures
    if (features) {
      return features.filter((f) => {
        return f.properties.admin_level === getters.getFirstSubLevel
      })
    }
    return []
  },
  getFirstSubLevelListFromMap(state, getters) {
    const features = getters.getSubLevelFeatures
    const firstSubLevel = getters.getFirstSubLevel
    const firstSubLevelType = getters.getFirstSubLevelType
    if (features && firstSubLevel && firstSubLevelType) {
      return features
        .filter((f) => f.properties.admin_level === firstSubLevel)
        .map((i) => ({
          ...JSON.parse(JSON.stringify(i.properties)),
          ...parseNames(i.properties.alltags),
        }))
    }
    return []
  },
  getSecondSubLevelListFromMap(state, getters) {
    const features = getters.getSubLevelFeatures
    const secondSubLevel = getters.getSecondSubLevel
    const secondSubLevelType = getters.getSecondSubLevelType
    if (features && secondSubLevel && secondSubLevelType) {
      return features
        .filter((f) => f.properties.admin_level === secondSubLevel)
        .map((i) => JSON.parse(JSON.stringify(i.properties)))
    }
    return []
  },
  getCountryCenter(state) {
    return state.countryCenter
  },
  getFirstSubLevel(state) {
    return state.firstSubLevel
  },
  getFirstSubLevelType(state) {
    return state.firstSubLevelType
  },
  getSecondSubLevel(state) {
    return state.secondSubLevel
  },
  getSecondSubLevelType(state) {
    return state.secondSubLevelType
  },
  getFacilities(state) {
    return [...state.facilities]
  },
  getFirstSubLevelList(state) {
    return state.firstSubLevelList
  },
  getSecondSubLevelList(state) {
    return state.secondSubLevelList
  },
}

const parseNames = (collection) => {
  const result = {}
  const names = ['name', 'name:es', 'name:pt', 'name:fr', 'name:ar']
  names.forEach((nk) => (result[nk] = collection[nk] || ''))
  return result
}

export const actions = {
  async loadGeoJSON({ commit, rootGetters }) {
    try {
      const country = rootGetters['admin/country/getData']
      const url =
        country.map_files.length && country.map_files.slice(-1)[0].map_file
      if (url) {
        const mediaIndex = url.indexOf('/media/')
        const proper = url.slice(mediaIndex)
        const { data } = await this.$axios.get(proper)
        Object.freeze(data)
        commit('SET_DATA', { type: 'geoJson', value: data })
      } else {
        commit('RESET_MAP_STATE')
      }
    } catch (e) {
      console.error('Map failed to load', e)
    }
  },
  setCountryCenter({ commit }, value) {
    value = value ? { ...value } : null
    commit('SET_DATA', { type: 'countryCenter', value })
  },
  setSecondSubLevelSource({ commit }, value) {
    commit('SET_DATA', { type: 'secondSubLevelSource', value })
  },
  setFirstSubLevel({ commit, getters }, value) {
    value = value || null
    commit('SET_DATA', { type: 'firstSubLevel', value })
    commit('SET_DATA', {
      type: 'firstSubLevelList',
      value: getters.getFirstSubLevelListFromMap,
    })
  },
  setFirstSubLevelType({ commit }, value) {
    value = value || null
    commit('SET_DATA', { type: 'firstSubLevelType', value })
  },
  setFirstSubLevelList({ commit }, value) {
    value = value || null
    commit('SET_DATA', { type: 'firstSubLevelList', value })
  },
  setSecondSubLevel({ commit, getters }, value) {
    value = value || null
    commit('SET_DATA', { type: 'secondSubLevel', value })
    commit('SET_DATA', {
      type: 'secondSubLevelList',
      value: getters.getSecondSubLevelListFromMap,
    })
  },
  setSecondSubLevelType({ commit }, value) {
    value = value || null
    commit('SET_DATA', { type: 'secondSubLevelType', value })
  },
  setSecondSubLevelList({ commit }, value) {
    value = value || null
    commit('SET_DATA', { type: 'secondSubLevelList', value })
  },
  updateSubLevelPolyCenter({ commit, getters }, { id, polyCenter }) {
    const index = getters.getFirstSubLevelList.findIndex((c) => c.id === id)
    commit('UPDATE_SUB_LEVELS_POLYCENTERS', { index, polyCenter })
  },
  setFacilities({ commit }, list) {
    list = list || []
    commit('SET_DATA', { type: 'facilities', value: list })
  },
  async saveMapData({ getters, rootGetters }) {
    const mapData = {
      second_sub_level_source: getters.getSecondSubLevelSource,
      polylabel: getters.getCountryCenter,
      first_sub_level: {
        admin_level: getters.getFirstSubLevel,
        name: getters.getFirstSubLevelType,
        elements: getters.getFirstSubLevelList,
      },
      second_sub_level: {
        admin_level: getters.getSecondSubLevel,
        name: getters.getSecondSubLevelType,
        elements: getters.getSecondSubLevelList,
      },
      facilities: getters.getFacilities,
    }

    try {
      const id = rootGetters['admin/country/getData'].id
      await this.$axios.patch(`/api/countries/${id}/`, { map_data: mapData })
    } catch (e) {
      console.error(e)
    }
  },
}
export const mutations = {
  SET_DATA: (state, { type, value }) => {
    state[type] = value
  },
  SET_SELECTED_COUNTRY: (state, id) => {
    state.id = id
  },
  SET_COUNTRY_DATA: (state, { id, map_file }) => {
    state.country = { id, map_file }
  },
  UPDATE_SUB_LEVELS_POLYCENTERS: (state, { index, polyCenter }) => {
    const updated = { ...state.firstSubLevelList[index], polyCenter }
    state.firstSubLevelList.splice(index, 1, updated)
  },
  RESET_MAP_STATE: (state) => {
    state.geoJson = null
    state.countryCenter = null
    state.firstSubLevel = ''
    state.firstSubLevelType = null
    state.secondSubLevel = ''
    state.secondSubLevelType = null
    state.facilities = []
    state.subLevelsPolyCenters = []
  },
}
