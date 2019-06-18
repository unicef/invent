export const state = () => ({
  geoJson: null,
  countryCenter: null,
  firstSubLevel: '',
  firstSubLevelType: null,
  secondSubLevel: '',
  secondSubLevelType: null,
  facilities: [],
  subLevelsPolyCenters: []
});

export const getters = {
  getGeoJson (state) {
    return state.geoJson;
  },
  getCountryBorder (state, getters) {
    const geoJson = getters.getGeoJson;
    if (geoJson && geoJson.features && geoJson.features.length > 0) {
      return geoJson.features.find(
        f => f.properties['admin_level'] === '2'
      );
    }
  },
  getSubLevelFeatures (state, getters) {
    const geoJson = getters.getGeoJson;
    let result = [];
    if (geoJson && geoJson.features && geoJson.features.length > 0) {
      result = geoJson.features.filter(
        f => f.properties['admin_level'] !== '2'
      );
    }
    if (geoJson && geoJson.features && result.length === 0) {
      result = geoJson.features.filter(
        f => f.properties['admin_level'] === '2'
      );
    }
    return result;
  },
  getSubLevels (state, getters) {
    const features = getters.getSubLevelFeatures;
    const levels = [];
    if (features) {
      for (const f of features) {
        if (!levels.includes(f.properties.admin_level)) {
          levels.push(f.properties.admin_level);
        }
      }
    }
    return levels;
  },
  getSubLevelsPolyCenters (state) {
    return [ ...state.subLevelsPolyCenters.filter(p => p.latlng).map(pc => ({ name: pc.name, latlng: { ...pc.latlng } })) ];
  },
  getFirstSubLevelMap (state, getters) {
    const features = getters.getSubLevelFeatures;
    if (features) {
      return features.filter(
        f => f.properties.admin_level === getters.getFirstSubLevel
      );
    }
    return [];
  },
  getFirstSubLevelList (state, getters) {
    const features = getters.getSubLevelFeatures;
    const firstSubLevel = getters.getFirstSubLevel;
    const firstSubLevelType = getters.getFirstSubLevelType;
    if (
      features &&
      firstSubLevel &&
      firstSubLevelType
    ) {
      return features
        .filter(f => f.properties.admin_level === firstSubLevel)
        .map(i => {
          const polyCenter = getters.getSubLevelsPolyCenters.find(pc => pc.name === i.properties.name);
          return { ...i.properties, polyCenter: polyCenter ? polyCenter.latlng : undefined };
        });
    }
    return [];
  },
  getSecondSubLevelList (state, getters) {
    const features = getters.getSubLevelFeatures;
    const secondSubLevel = getters.getSecondSubLevel;
    const secondSubLevelType = getters.getSecondSubLevelType;
    if (
      features &&
      secondSubLevel &&
      secondSubLevelType
    ) {
      return features
        .filter(f => f.properties.admin_level === secondSubLevel)
        .map(i => i.properties);
    }
    return [];
  },
  getCountryCenter (state) {
    return state.countryCenter;
  },
  getFirstSubLevel (state) {
    return state.firstSubLevel;
  },
  getFirstSubLevelType (state) {
    return state.firstSubLevelType;
  },
  getSecondSubLevel (state) {
    return state.secondSubLevel;
  },
  getSecondSubLevelType (state) {
    return state.secondSubLevelType;
  },
  getFacilities (state) {
    return [...state.facilities];
  }

};

const parseNames = (collection) => {
  const result = {};
  const nameKeys = Object.keys(collection).filter(k => k.includes('name:'));
  nameKeys.forEach(nk => (result[nk] = collection[nk]));
  return result;
};

export const actions = {
  async loadGeoJSON ({ commit, rootGetters }) {
    try {
      const country = rootGetters['admin/country/getData'];
      const url = country.map_files.length && country.map_files.slice(-1)[0].map_file;
      if (url) {
        const mediaIndex = url.indexOf('/media/');
        const proper = url.slice(mediaIndex);
        const { data } = await this.$axios.get(proper);
        Object.freeze(data);
        commit('UPDATE_GEO_JSON', data);
      } else {
        commit('RESET_MAP_STATE');
      }
    } catch (e) {
      console.error('Map failed to load', e);
    }
  },
  setCountryCenter ({ commit }, value) {
    value = value ? { ...value } : null;
    commit('SET_COUNTRY_CENTER', value);
  },
  setFirstSubLevel ({ commit }, value) {
    value = value || null;
    commit('SET_FIRST_SUB_LEVEL', value);
  },
  setFirstSubLevelType ({ commit }, value) {
    value = value || null;
    commit('SET_FIRST_SUB_LEVEL_TYPE', value);
  },
  setSecondSubLevel ({ commit }, value) {
    value = value || null;
    commit('SET_SECOND_SUB_LEVEL', value);
  },
  setSecondSubLevelType ({ commit }, value) {
    value = value || null;
    commit('SET_SECOND_SUB_LEVEL_TYPE', value);
  },
  parseSubLevelsPolyCenters ({ dispatch }, value) {
    const polyCenters = value.elements.map(e => ({ name: e.name, latlng: e.polyCenter }));
    dispatch('setSubLevelsPolyCenters', polyCenters);
  },
  setSubLevelsPolyCenters ({ commit }, value) {
    value = value || [];
    commit('SET_SUB_LEVELS_POLYCENTERS', value);
  },
  updateSubLevelPolyCenter ({ commit, getters }, { name, latlng }) {
    const current = getters.getSubLevelsPolyCenters;
    const index = current.findIndex(c => c.name === name);
    commit('UPDATE_SUB_LEVELS_POLYCENTERS', { index, data: { name, latlng } });
  },
  setFacilities ({ commit }, list) {
    list = list || [];
    commit('SET_FACILITIES', list);
  },
  async saveMapData ({ getters, rootGetters }) {
    const first = getters.getFirstSubLevelList.map((f, index) => {
      return {
        id: f.id || index,
        name: f.name,
        polyCenter: f.polyCenter,
        ...parseNames(f.alltags)
      };
    });
    const second = getters.getSecondSubLevelList.map((s, index) => {
      return {
        id: s.id || index,
        name: s.name,
        ...parseNames(s.alltags)
      };
    });
    const mapData = {
      polylabel: getters.getCountryCenter,
      first_sub_level: {
        admin_level: getters.getFirstSubLevel,
        name: getters.getFirstSubLevelType,
        elements: first
      },
      second_sub_level: {
        admin_level: getters.getSecondSubLevel,
        name: getters.getSecondSubLevelType,
        elements: second
      },
      facilities: getters.getFacilities
    };

    try {
      const id = rootGetters['admin/country/getData'].id;
      await this.$axios.patch(`/api/countries/${id}/`, { map_data: mapData });
    } catch (e) {
      console.error(e);
    }
    this.saving = false;
  }
};
export const mutations = {
  SET_SELECTED_COUNTRY: (state, id) => {
    state.id = id;
  },
  SET_COUNTRY_DATA: (state, { id, map_file }) => {
    state.country = { id, map_file };
  },
  SET_COUNTRY_CENTER: (state, data) => {
    state.countryCenter = data;
  },
  SET_FIRST_SUB_LEVEL: (state, data) => {
    state.firstSubLevel = data;
  },
  SET_FIRST_SUB_LEVEL_TYPE: (state, data) => {
    state.firstSubLevelType = data;
  },
  SET_SECOND_SUB_LEVEL: (state, data) => {
    state.secondSubLevel = data;
  },
  SET_SECOND_SUB_LEVEL_TYPE: (state, data) => {
    state.secondSubLevelType = data;
  },
  UPDATE_GEO_JSON: (state, data) => {
    state.geoJson = data;
  },
  SET_FACILITIES: (state, data) => {
    state.facilities = data;
  },
  SET_SUB_LEVELS_POLYCENTERS: (state, data) => {
    state.subLevelsPolyCenters = data;
  },
  UPDATE_SUB_LEVELS_POLYCENTERS: (state, { index, data }) => {
    state.subLevelsPolyCenters.splice(index, 1, data);
  },
  RESET_MAP_STATE: state => {
    state.geoJson = null;
    state.countryCenter = null;
    state.firstSubLevel = '';
    state.firstSubLevelType = null;
    state.secondSubLevel = '';
    state.secondSubLevelType = null;
    state.facilities = [];
    state.subLevelsPolyCenters = [];
  }
};
