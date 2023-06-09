import find from 'lodash/find'

export const state = () => ({
  profiles: [],
  search_filters: [],
  languages: [],
  projectSearch: [],
  thematic_overview: [],
  axis: [],
  domains: [],
  landing_page_defaults: {},
  sub_level_types: [],
  organisations: [],
  donors: [],
  regions: [],
  unicef_regions: [],
  partner_types: [],
  link_types: [],
  donorsLibrary: {},
  review_questions: {},
  review_statuses: {},
  scalePhases: [],
  solutionPhases: [],
})

export const getters = {
  getUserProfiles: (state) => {
    return state.profiles ? [...state.profiles.filter((p) => p.name)] : []
  },
  getUserProfilesNoFilter: (state) => {
    return state.profiles
  },
  getUserProfilesWithLabel: (state) => {
    const labelFullInfo = ['job_title', 'department', 'country']

    const labeledProfiles = state.profiles.map((user) => {
      const username = user.name ? `${user.name} ` : ''
      const useremail = user.email ? `(${user.email})` : ''
      let concLabel = username + useremail

      let concFullInfo = []
      labelFullInfo.forEach(
        (field) => (concFullInfo = user[field] ? [...concFullInfo, ` ${user[field]}`] : concFullInfo)
      )
      return { ...user, label: concLabel, info: concFullInfo.toString(), value: concLabel }
    })
    return labeledProfiles
  },
  getUserProfileDetails: (state, getters) => (id) => getters.getUserProfiles.find((u) => u.id === id),
  getSearchResult: (state) => {
    const search = state.projectSearch ? state.projectSearch : []
    return search.map((s) => {
      return {
        ...s,
      }
    })
  },
  getLanguages: (state) => {
    return state.languages.map((l) => ({ ...l, flag: `/static/flags/${l.flag}` })).filter((l) => l.code !== 'ar')
  },
  getLanguageDetails: (state, getters) => (code) => {
    return getters.getLanguages.find((l) => l.code === code)
  },
  getSearchFilters: (state) => {
    return [...state.search_filters]
  },
  getLandingPageDefaults: (state) => {
    return { ...state.landing_page_defaults }
  },
  getAxis: (state) => {
    return [...state.axis]
  },
  getDomains: (state) => {
    return [...state.domains]
  },
  getReviewStatuses: (state) => {
    return Object.assign({}, ...state.review_statuses.map(({ id, text }) => ({ [id]: text })))
  },
  getThematicOverview: (state) => {
    const th = state.thematic_overview
    return th.categories
      ? th.categories.map((cat) => ({
          ...cat,
          domains: th.sub_categories.filter((sb) => sb.category === cat.id),
        }))
      : []
  },
  getDomainsForThematic: (state, getters) => {
    const axis = getters.getAxis
    const domains = getters.getDomains
    const thematic_specific = getters.getThematicOverview
    return [
      ...thematic_specific.map((t) => ({ name: t.name, domains: t.domains })),
      ...axis.map((a) => ({
        name: a.name,
        domains: domains.filter((d) => d.axis === a.id).map((df) => ({ name: df.name })),
      })),
    ]
  },
  getSubLevelTypes: (state) => {
    return [...state.sub_level_types.map((t) => ({ ...t }))]
  },
  getOrganisations: (state) => {
    return [...state.organisations.map((o) => ({ ...o }))]
  },
  getOrganisationDetails: (state, getters) => (id) => {
    const o = getters.getOrganisations.find((org) => org.id === id)
    return o ? { ...o } : undefined
  },
  getDonors: (state) => state.donors,
  getDonorDetails: (state) => (id) => ({
    ...state.donors.find((d) => d.id === id),
    ...state.donorsLibrary[id],
  }),
  getRegions: (state) => state.regions,
  getRegionDetails: (state) => (id) => ({
    ...state.regions.find((r) => r.id === id),
  }),
  getUnicefRegions: (state) => state.unicef_regions,
  getLinkTypes: (state) => state.link_types,
  getPartnerTypes: (state) => state.partner_types,
  getUnicefDonor: (state) => find(state.donors, ({ name }) => name === 'UNICEF'),
  getUnicefOrganisation: (state) => find(state.organisations, ({ name }) => name === 'UNICEF'),
  getSolutionPhases: (state) => state.solutionPhases,
}

export const actions = {
  async loadUserProfiles({ commit, state }, force = false) {
    try {
      if (!state.profiles || state.profiles.length === 0 || force) {
        const { data } = await this.$axios.get('/api/userprofiles/')
        commit('SET_USER_PROFILES', data)
      }
    } catch (e) {
      console.error('system/loadUserProfiles failed')
    }
  },

  async loadStaticData({ state, commit, dispatch }) {
    if (state.unicef_regions.length > 0 && state.solutionPhases > 0) return
    try {
      const { data } = await this.$axios.get('/api/static-data/')
      commit('SET_AXIS', data.axis)
      commit('SET_DATA', { key: 'partner_types', value: data.partner_types })
      commit('SET_DATA', { key: 'link_types', value: data.link_types })
      commit('SET_DATA', {
        key: 'review_questions',
        value: data.review_questions,
      })
      commit('SET_DATA', {
        key: 'review_statuses',
        value: data.review_status,
      })
      commit('SET_DOMAINS', data.domains)
      commit('SET_LANDING_PAGE_DEFAULTS', data.landing_page_defaults)
      commit('SET_LANGUAGES', data.languages)
      commit('SET_THEMATIC_OVERVIEW', data.thematic_overview)
      commit('SET_SUB_LEVEL_TYPES', data.sub_level_types)
      commit('SET_REGIONS', data.unicef_regions)
      commit('SET_DATA', { key: 'unicef_regions', value: data.unicef_regions })
      commit('SET_DATA', { key: 'scalePhases', value: data.scale_phases })
      commit('SET_DATA', { key: 'solutionPhases', value: data.solution_phases })
      // columns are coming from
      // console.log(data.dashboard_columns)

      dispatch('dashboard/setDashboardColumns', data.dashboard_columns, {
        root: true,
      })
    } catch (e) {
      console.error('system/loadStaticData failed')
    }
  },

  async loadOrganisations({ state, commit, rootGetters }) {
    if (state.organisations.length > 0) return
    const profile = rootGetters['user/getProfile']
    if (profile) {
      try {
        const { data } = await this.$axios.get(`/api/organisations/`)
        commit('SET_SYSTEM_ORGANISATIONS', data)
      } catch (e) {
        console.error('system/loadOrganisations failed')
      }
    }
  },
  async loadDonors({ state, commit }) {
    if (state.donors.length > 0) return
    try {
      const { data } = await this.$axios.get(`/api/landing-donor/`)
      commit('SET_DONORS', data)
    } catch (e) {
      console.error('system/loadDonors failed')
    }
  },
  async loadDonorDetails({ commit, state }, id) {
    if (id && !state.donorsLibrary[id]) {
      try {
        const { data } = await this.$axios.get(`/api/landing-donor/${id}/`)
        commit('SET_DONOR_DETAILS', { id, data })
      } catch (e) {
        console.error('system/loadDonorDetails failed')
      }
    }
  },
  async addOrganisation({ dispatch, getters }, name) {
    try {
      await this.$axios.post('/api/organisations/', { name })
    } catch (e) {
      console.error('system/addOrganisation failed')
    } finally {
      await dispatch('loadOrganisations')
    }
    const org = getters.getOrganisations.find((o) => o.name === name)
    if (org) {
      return Promise.resolve(org)
    } else {
      const error = new Error('Organisation saving / fetching failed, could not find the organisation')
      return Promise.reject(error)
    }
  },
}

export const mutations = {
  SET_DATA: (state, { value, key }) => {
    state[key] = value
  },
  SET_USER_PROFILES: (state, value) => {
    state.profiles = value
  },

  SET_AXIS: (state, value) => {
    state.axis = value
  },

  SET_DOMAINS: (state, value) => {
    state.domains = value
  },

  SET_LANDING_PAGE_DEFAULTS: (state, value) => {
    state.landing_page_defaults = value
  },

  SET_LANGUAGES: (state, value) => {
    state.languages = value
  },

  SET_THEMATIC_OVERVIEW: (state, value) => {
    state.thematic_overview = value
  },

  SET_SUB_LEVEL_TYPES: (state, value) => {
    state.sub_level_types = value
  },

  SET_SYSTEM_ORGANISATIONS: (state, value) => {
    state.organisations = value
  },
  SET_DONORS: (state, donors) => {
    state.donors = donors
  },
  SET_DONOR_DETAILS: (state, { id, data }) => {
    state.donorsLibrary = { ...state.donorsLibrary, [id]: data }
  },
  SET_REGIONS: (state, regions) => {
    state.regions = regions
  },
}
