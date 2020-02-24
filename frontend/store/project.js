import Vue from 'vue';
import get from 'lodash/get';
import { apiReadParser, apiWriteParser, APIError } from '../utilities/api';
import { projectFields } from '../utilities/projects';

const cleanState = () => ({
  ...projectFields(),
  country_answers: [],
  donors_answers: [],
  published: null,
  original: null
});

export const state = () => ({
  ...cleanState(),
  loading: false
});

export const getters = {
  getProjectData: (state, getters) => ({
    ...state,
    donors: getters.getDonors,
    interoperability_links: getters.getInteroperabilityLinks,
    published: undefined,
    loading: undefined,
    country_answers: undefined,
    donor_answers: undefined,
    original: undefined
  }),
  getName: state => state.name,
  getOrganisation: state => state.organisation,
  getCountry: state => state.country,
  getFieldOffice: state => state.field_office,
  getModified: state => state.modified,
  getImplementationOverview: state => state.implementation_overview,
  getStartDate: state => state.start_date,
  getEndDate: state => state.end_date,
  getContactName: state => state.contact_name,
  getContactEmail: state => state.contact_email,
  getTeam: state => state.team,
  getViewers: state => state.viewers,
  getGoalArea: state => state.goal_area,
  getResultArea: state => state.result_area,
  getGoalAreaDetails: (state, getters, rootState, rootGetters) => {
    const selected = rootGetters['projects/getGoalAreas'].find(ga => ga.id === state.goal_area);
    return selected || {};
  },
  getCapabilityLevels: state => state.capability_levels,
  getCapabilityCategories: state => state.capability_categories,
  getCapabilitySubcategories: state => state.capability_subcategories,
  getPlatforms: state => state.platforms.length === 0 ? [null] : state.platforms,
  getDigitalHealthInterventions: state => [...state.dhis],
  getHealthFocusAreas: state => state.health_focus_areas,
  getHscChallenges: state => state.hsc_challenges,
  getDonors: state => {
    const cleaned = state.donors.filter(d => d !== 20);
    return [20, ...cleaned];
  },
  getDonorsAnswers: state => state.donors_answers ? [...state.donors_answers] : [],
  getDonorsAnswerDetails: (state, getters) => id => getters.getDonorsAnswers.find(da => da.question_id === id),
  getAllDonorsAnswers: (state, getters, rootState, rootGetters) => {
    const donors = getters.getDonors
      .map(d => rootGetters['system/getDonorDetails'](d))
      .filter(d => d.donor_questions);
    if (donors) {
      return donors.reduce((a, c) => {
        a.push(...c.donor_questions.map(dq => {
          const answer = getters.getDonorsAnswerDetails(dq.id);
          return { question_id: dq.id, answer: answer ? answer.answer : [], donor_id: c.id };
        }));
        return a;
      }, []);
    }
  },
  getPublishedDonorsAnswerDetails: (state, getters) => id => getters.getPublished.donor_custom_answers.find(ca => ca.question_id === id),
  getPublished: state => ({ ...state.published, team: state.team, viewers: state.viewers }),
  getLoading: state => state.loading,
  getOriginal: state => state.original
};

export const actions = {
  async loadProject ({ commit, dispatch, rootGetters }, id) {
    const userProject = rootGetters['projects/getUserProjectList'].find(p => p.id === id);
    const { data } = userProject && userProject.id ? { data: userProject } : await this.$axios.get(`/api/projects/${id}/`);
    commit('SET_ORIGINAL', Object.freeze(data));
    const clean = cleanState();
    const donorsToFetch = new Set([20]);
    if (data.draft) {
      const draft = { ...clean, ...apiReadParser(data.draft) };
      draft.donors.forEach(d => donorsToFetch.add(d));
      commit('INIT_PROJECT', draft);
    }
    if (data.published) {
      const published = { ...clean, ...apiReadParser(data.published) };
      published.donors.forEach(d => donorsToFetch.add(d));
      commit('SET_PUBLISHED', Object.freeze(published));
    }
    await Promise.all([
      ...[...donorsToFetch].map(df => dispatch('system/loadDonorDetails', df, { root: true })),
      dispatch('loadTeamViewers', id)
    ]);
  },
  async loadTeamViewers ({ commit, rootGetters }, projectId) {
    const profile = rootGetters['user/getProfile'];
    if (profile) {
      const { data } = await this.$axios.get(`/api/projects/${projectId}/groups/`);
      commit('SET_TEAM', data.team);
      commit('SET_VIEWERS', data.viewers);
    }
  },
  async resetProjectState ({ commit, rootGetters, dispatch }) {
    const clean = cleanState();
    const profile = rootGetters['user/getProfile'];
    if (profile) {
      clean.country = profile.country;
      clean.team = [profile.id];
      clean.organisation = 56;
      clean.donors = [20];
      await Promise.all([
        dispatch('countries/loadCountryDetails', profile.country, { root: true }),
        dispatch('system/loadDonorDetails', 20, { root: true })
      ]);
    }
    commit('INIT_PROJECT', clean);
    commit('SET_TEAM', clean.team);
    commit('SET_VIEWERS', clean.viewers);
  },
  initProjectState ({ commit }, value) {
    commit('INIT_PROJECT', value);
    commit('SET_TEAM', value.team);
    commit('SET_VIEWERS', value.viewers);
  },
  setGoalArea ({ commit }, value) {
    commit('SET_DATA', { key: 'goal_area', value });
    commit('SET_DATA', { key: 'result_area', value: null });
    commit('SET_DATA', { key: 'capability_levels', value: [] });
    commit('SET_DATA', { key: 'capability_categories', value: [] });
    commit('SET_DATA', { key: 'capability_subcategories', value: [] });
  },
  setResultArea ({ commit }, value) {
    commit('SET_DATA', { key: 'result_area', value });
  },
  setFieldOffice ({ commit }, value) {
    commit('SET_DATA', { key: 'field_office', value });
  },
  setCapabilityLevels ({ commit }, value) {
    commit('SET_DATA', { key: 'capability_levels', value });
  },
  setCapabilityCategories ({ commit }, value) {
    commit('SET_DATA', { key: 'capability_categories', value });
  },
  setCapabilitySubcategories ({ commit }, value) {
    commit('SET_DATA', { key: 'capability_subcategories', value });
  },
  setName ({ commit }, value) {
    commit('SET_NAME', value);
  },
  setOrganisation ({ commit }, value) {
    commit('SET_ORGANISATION', value);
  },
  setCountry ({ commit, dispatch }, value) {
    dispatch('countries/loadCountryDetails', value, { root: true });
    commit('SET_COUNTRY', value);
  },
  setImplementationOverview ({ commit }, value) {
    commit('SET_IMPLEMENTATION_OVERVIEW', value);
  },
  setStartDate ({ commit }, value) {
    commit('SET_START_DATE', value);
  },
  setEndDate ({ commit }, value) {
    commit('SET_END_DATE', value);
  },
  setContactName ({ commit }, value) {
    commit('SET_CONTACT_NAME', value);
  },
  setContactEmail ({ commit }, value) {
    commit('SET_CONTACT_EMAIL', value);
  },
  setTeam ({ commit }, value) {
    commit('SET_TEAM', value);
  },
  setViewers ({ commit }, value) {
    commit('SET_VIEWERS', value);
  },
  setPlatforms ({ commit }, value) {
    commit('SET_PLATFORMS', value);
  },
  setDigitalHealthInterventions ({ commit }, value) {
    commit('SET_DIGITAL_HEALTH_INTERVENTIONS', value);
  },
  setHealthFocusAreas ({ commit }, value) {
    commit('SET_HEALTH_FOCUS_AREAS', value);
  },
  setHscChallenges ({ commit }, value) {
    commit('SET_HSC_CHALLENGES', value);
  },
  setDonors ({ commit, dispatch }, value) {
    value.forEach(d => dispatch('system/loadDonorDetails', d, { root: true }));
    commit('SET_DONORS', value);
  },
  setImplementationDates ({ commit }, value) {
    commit('SET_IMPLEMENTATION_DATES', value);
  },
  setPublished ({ commit }, value) {
    commit('SET_PUBLISHED', value);
  },
  setLoading ({ commit }, value) {
    commit('SET_LOADING', value);
  },
  setDonorAnswer ({ commit, getters }, answer) {
    const index = getters.getDonorsAnswers.findIndex(da => da.question_id === answer.question_id);
    if (index > -1) {
      commit('UPDATE_DONOR_ANSWER', { answer, index });
    } else {
      commit('ADD_DONOR_ANSWER', answer);
    }
  },
  async verifyOrganisation ({ dispatch }, organisation) {
    try {
      if (organisation && isNaN(organisation)) {
        const org = await dispatch('system/addOrganisation', organisation, { root: true });
        return org.id;
      }
      return organisation;
    } catch (e) {
      console.log('project/verifyOrganisation failed');
      return Promise.reject(APIError('organisation', 'Failed to save the organisation'));
    }
  },
  async saveTeamViewers ({ getters, commit, dispatch }, id) {
    const teamViewers = {
      team: getters.getTeam.filter(d => typeof d === 'number'),
      viewers: getters.getViewers.filter(d => typeof d === 'number'),
      new_team_emails: getters.getTeam.filter(d => typeof d === 'string'),
      new_viewer_emails: getters.getViewers.filter(d => typeof d === 'string')
    };
    const { data } = await this.$axios.put(`/api/projects/${id}/groups/`, teamViewers);
    commit('SET_TEAM', data.team);
    commit('SET_VIEWERS', data.viewers);
    return dispatch('user/updateTeamViewers', { ...data, id }, { root: true });
  },
  async createProject ({ getters, dispatch }) {
    dispatch('setLoading', 'draft');
    const draft = getters.getProjectData;
    draft.organisation = 56;
    const parsed = apiWriteParser(draft, getters.getAllCountryAnswers, getters.getAllDonorsAnswers);
    const { data } = await this.$axios.post(`api/projects/draft/${draft.country}/`, parsed);
    dispatch('projects/addProjectToList', data, { root: true });
    await dispatch('saveTeamViewers', data.id);
    dispatch('setLoading', false);
    return data.id;
  },
  async saveDraft ({ getters, dispatch }, id) {
    dispatch('setLoading', 'draft');
    const draft = getters.getProjectData;
    draft.organisation = 56;
    const parsed = apiWriteParser(draft, getters.getAllCountryAnswers, getters.getAllDonorsAnswers);
    const { data } = await this.$axios.put(`api/projects/draft/${id}/${draft.country}/`, parsed);
    const isUserProject = await dispatch('saveTeamViewers', id);
    if (isUserProject) {
      dispatch('projects/updateProject', data, { root: true });
    } else {
      dispatch('projects/removeProject', data.id, { root: true });
    }
    dispatch('setLoading', false);
  },
  async publishProject ({ getters, dispatch, commit }, id) {
    dispatch('setLoading', 'publish');
    const draft = getters.getProjectData;
    draft.organisation = 56;
    const parsed = apiWriteParser(draft, getters.getAllCountryAnswers, getters.getAllDonorsAnswers);
    const { data } = await this.$axios.put(`/api/projects/publish/${id}/${draft.country}/`, parsed);
    const isUserProject = await dispatch('saveTeamViewers', id);
    const parsedResponse = apiReadParser(data.draft);
    commit('SET_PUBLISHED', Object.freeze(parsedResponse));
    if (isUserProject) {
      dispatch('projects/updateProject', data, { root: true });
    } else {
      dispatch('projects/removeProject', data.id, { root: true });
    }
    dispatch('setLoading', false);
  },
  async discardDraft ({ getters, dispatch, commit }, id) {
    dispatch('setLoading', 'discard');
    const published = getters.getPublished;
    const parsed = apiWriteParser(published, published.country_custom_answers, published.donor_custom_answers);
    const { data } = await this.$axios.put(`api/projects/draft/${id}/${published.country}/`, parsed);
    const parsedResponse = apiReadParser(data.draft);
    commit('INIT_PROJECT', parsedResponse);
    dispatch('projects/updateProject', data, { root: true });
    dispatch('setLoading', false);
  }
};

export const mutations = {
  SET_DATA: (state, { value, key }) => {
    state[key] = value;
  },
  SET_NAME: (state, name) => {
    state.name = name;
  },
  SET_ORGANISATION: (state, organisation) => {
    state.organisation = organisation;
  },
  SET_COUNTRY: (state, country) => {
    state.country = country;
  },
  SET_IMPLEMENTATION_OVERVIEW: (state, implementation_overview) => {
    state.implementation_overview = implementation_overview;
  },
  SET_START_DATE: (state, start_date) => {
    state.start_date = start_date;
  },
  SET_END_DATE: (state, end_date) => {
    state.end_date = end_date;
  },
  SET_CONTACT_NAME: (state, contact_name) => {
    state.contact_name = contact_name;
  },
  SET_CONTACT_EMAIL: (state, contact_email) => {
    state.contact_email = contact_email;
  },
  SET_TEAM: (state, team) => {
    const items = typeof team === 'string' ? state.team.concat([team]) : team;
    Vue.set(state, 'team', [...items]);
  },
  SET_VIEWERS: (state, viewer) => {
    const items = typeof viewer === 'string' ? state.viewers.concat([viewer]) : viewer;
    Vue.set(state, 'viewers', [...items]);
  },
  SET_PLATFORMS: (state, platforms) => {
    Vue.set(state, 'platforms', [...platforms]);
  },
  SET_DIGITAL_HEALTH_INTERVENTIONS: (state, dhi) => {
    Vue.set(state, 'dhis', [...dhi]);
  },
  SET_HEALTH_FOCUS_AREAS: (state, health_focus_areas) => {
    Vue.set(state, 'health_focus_areas', [...health_focus_areas]);
  },
  SET_HSC_CHALLENGES: (state, hsc_challenges) => {
    Vue.set(state, 'hsc_challenges', [...hsc_challenges]);
  },
  SET_DONORS: (state, donors) => {
    Vue.set(state, 'donors', [...donors]);
  },
  SET_IMPLEMENTATION_DATES: (state, implementation_dates) => {
    state.implementation_dates = implementation_dates;
  },
  ADD_DONOR_ANSWER: (state, answer) => {
    state.donors_answers.push(answer);
  },
  UPDATE_DONOR_ANSWER: (state, { answer, index }) => {
    state.donors_answers.splice(index, 1, answer);
  },
  SET_PUBLISHED: (state, published) => {
    Vue.set(state, 'published', { ...published });
  },
  SET_LOADING: (state, loading) => {
    state.loading = loading;
  },
  INIT_PROJECT: (state, project) => {
    state.name = get(project, 'name', '');
    state.organisation = get(project, 'organisation', 56);
    state.country = get(project, 'country', null);
    state.modified = get(project, 'modified', null);
    state.field_office = get(project, 'field_office', null);
    state.implementation_overview = get(project, 'implementation_overview', '');
    state.start_date = get(project, 'start_date', '');
    state.end_date = get(project, 'end_date', '');
    state.contact_name = get(project, 'contact_name', '');
    state.contact_email = get(project, 'contact_email', '');
    state.team = get(project, 'team', []);
    state.viewers = get(project, 'viewers', []);
    state.goal_area = get(project, 'goal_area', null);
    state.result_area = get(project, 'result_area', null);
    state.capability_levels = get(project, 'capability_levels', []);
    state.capability_categories = get(project, 'capability_categories', []);
    state.capability_subcategories = get(project, 'capability_subcategories', []);
    state.platforms = get(project, 'platforms', []);
    state.dhis = get(project, 'dhis', []);
    state.health_focus_areas = get(project, 'health_focus_areas', []);
    state.hsc_challenges = get(project, 'hsc_challenges', []);
    state.modified = get(project, 'modified', new Date());
    state.donors = get(project, 'donors', []);
    state.country_answers = get(project, 'country_custom_answers', []);
    state.donors_answers = get(project, 'donor_custom_answers', []);
  },
  SET_ORIGINAL: (state, project) => {
    state.original = project;
  }

};
