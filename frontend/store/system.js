export const state = () => ({
  profiles: [],
  search_filters: [],
  languages: [],
  projectSearch: [],
  thematic_overview: [],
  axis: [],
  domains: [],
  landing_page_defaults: {},
  toolkit_questions: [],
  sub_level_types: [],
  organisations: [],
  donors: [],
  regions: [],
  unicef_regions: [],
  donorsLibrary: {}
});

export const getters = {
  getUserProfiles: state => {
    return state.profiles ? [ ...state.profiles.filter(p => p.name) ] : [];
  },
  getUserProfilesNoFilter: state => {
    return state.profiles;
  },
  getUserProfileDetails: (state, getters) => id => getters.getUserProfiles.find(u => u.id === id),
  getSearchResult: state => {
    const search = state.projectSearch ? state.projectSearch : [];
    return search.map(s => {
      return {
        ...s
      };
    });
  },
  getLanguages: state => {
    return state.languages
      .map(l => ({ ...l, flag: `/static/flags/${l.flag}` }))
      .filter(l => l.code !== 'ar');
  },

  getLanguageDetails: (state, getters) => code => {
    return getters.getLanguages.find(l => l.code === code);
  },
  getSearchFilters: state => {
    return [...state.search_filters];
  },
  getLandingPageDefaults: state => {
    return { ...state.landing_page_defaults };
  },
  getAxis: state => {
    return [...state.axis];
  },
  getDomains: state => {
    return [...state.domains];
  },
  getQuestions: state => {
    return [...state.toolkit_questions];
  },
  getThematicOverview: state => {
    const th = state.thematic_overview;
    return th.categories
      ? th.categories.map(cat => ({ ...cat, domains: th.sub_categories.filter(sb => sb.category === cat.id) }))
      : [];
  },
  getDomainsForThematic: (state, getters) => {
    const axis = getters.getAxis;
    const domains = getters.getDomains;
    const thematic_specific = getters.getThematicOverview;
    return [
      ...thematic_specific.map(t => ({ name: t.name, domains: t.domains })),
      ...axis.map(a => ({
        name: a.name,
        domains: domains
          .filter(d => d.axis === a.id)
          .map(df => ({ name: df.name }))
      }))];
  },
  getSubLevelTypes: state => {
    return [...state.sub_level_types.map(t => ({ ...t }))];
  },
  getOrganisations: state => {
    return [...state.organisations.map(o => ({ ...o }))];
  },
  getOrganisationDetails: (state, getters) => id => {
    const o = getters.getOrganisations.find(org => org.id === id);
    return o ? { ...o } : undefined;
  },
  getDonors: state => state.donors,
  getDonorDetails: state => id => ({ ...state.donors.find(d => d.id === id), ...state.donorsLibrary[id] }),
  getRegions: state => state.regions,
  getRegionDetails: state => id => ({ ...state.regions.find(r => r.id === id) }),
  getUnicefRegions: state => state.unicef_regions
};

export const actions = {

  async loadUserProfiles ({ commit, state }, force = false) {
    try {
      if (!state.profiles || state.profiles.length === 0 || force) {
        const { data } = await this.$axios.get('/api/userprofiles/');
        commit('SET_USER_PROFILES', data);
      }
    } catch (e) {
      console.error('system/loadUserProfiles failed');
    }
  },

  async loadStaticData ({ commit, dispatch }) {
    try {
      const { data } = await this.$axios.get('/api/static-data/');
      commit('SET_AXIS', data.axis);
      commit('SET_DOMAINS', data.domains);
      commit('SET_LANDING_PAGE_DEFAULTS', data.landing_page_defaults);
      commit('SET_LANGUAGES', data.languages);
      commit('SET_THEMATIC_OVERVIEW', data.thematic_overview);
      commit('SET_TOOLKIT_QUESTIONS', data.toolkit_questions);
      commit('SET_SUB_LEVEL_TYPES', data.sub_level_types);
      commit('SET_REGIONS', data.unicef_regions);
      commit('SET_DATA', { key: 'unicef_regions', value: data.unicef_regions });
      dispatch('dashboard/setDashboardColumns', data.dashboard_columns, { root: true });
    } catch (e) {
      console.error('system/loadStaticData failed');
    }
  },

  async loadOrganisations ({ commit, rootGetters }) {
    const profile = rootGetters['user/getProfile'];
    if (profile) {
      try {
        const { data } = await this.$axios.get(`/api/organisations/`);
        commit('SET_SYSTEM_ORGANISATIONS', data);
      } catch (e) {
        console.error('system/loadOrganisations failed');
      }
    }
  },
  async loadDonors ({ commit }) {
    try {
      const { data } = await this.$axios.get(`/api/landing-donor/`);
      commit('SET_DONORS', data);
    } catch (e) {
      console.error('system/loadDonors failed');
    }
  },
  async loadDonorDetails ({ commit, state }, id) {
    if (id && !state.donorsLibrary[id]) {
      try {
        const { data } = await this.$axios.get(`/api/landing-donor/${id}/`);
        commit('SET_DONOR_DETAILS', { id, data });
      } catch (e) {
        console.error('system/loadDonorDetails failed');
      }
    }
  },
  async addOrganisation ({ dispatch, getters }, name) {
    try {
      await this.$axios.post('/api/organisations/', { name });
    } catch (e) {
      console.error('system/addOrganisation failed');
    } finally {
      await dispatch('loadOrganisations');
    }
    const org = getters.getOrganisations.find(o => o.name === name);
    if (org) {
      return Promise.resolve(org);
    } else {
      const error = new Error('Organisation saving / fetching failed, could not find the organisation');
      return Promise.reject(error);
    }
  }
};

export const mutations = {
  SET_DATA: (state, { value, key }) => {
    state[key] = value;
  },
  SET_USER_PROFILES: (state, value) => {
    state.profiles = value;
  },

  SET_AXIS: (state, value) => {
    state.axis = value;
  },

  SET_DOMAINS: (state, value) => {
    state.domains = value;
  },

  SET_LANDING_PAGE_DEFAULTS: (state, value) => {
    state.landing_page_defaults = value;
  },

  SET_LANGUAGES: (state, value) => {
    state.languages = value;
  },

  SET_THEMATIC_OVERVIEW: (state, value) => {
    state.thematic_overview = value;
  },

  SET_TOOLKIT_QUESTIONS: (state, value) => {
    state.toolkit_questions = value;
  },

  SET_SUB_LEVEL_TYPES: (state, value) => {
    state.sub_level_types = value;
  },

  SET_SYSTEM_ORGANISATIONS: (state, value) => {
    state.organisations = value;
  },
  SET_DONORS: (state, donors) => {
    state.donors = donors;
  },
  SET_DONOR_DETAILS: (state, { id, data }) => {
    state.donorsLibrary = { ...state.donorsLibrary, [id]: data };
  },
  SET_REGIONS: (state, regions) => {
    state.regions = regions;
  }
};
