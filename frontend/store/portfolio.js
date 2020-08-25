import Vue from "vue";
import get from "lodash/get";
import { apiReadParser, apiWriteParser, APIError } from "../utilities/api";

export const state = () => ({
  loading: false,
  name: "",
  description: "",
  status: [],
  icon: null,
  managers: [],
  statements: []
});

export const getters = {
  getName: state => state.name,
  getDescription: state => state.description,
  getStatus: state => state.status,
  getIcon: state => state.icon,
  getManagers: state => state.managers,
  getStatements: state => state.statements,
  getLoading: state => state.loading
};

export const actions = {
  setName({ commit }, value) {
    commit("SET_NAME", value);
  },
  setDescription({ commit }, value) {
    commit("SET_DESCRIPTION", value);
  },
  setStatus({ commit, dispatch }, value) {
    commit("SET_STATUS", value);
  },
  setIcon({ commit, dispatch }, value) {
    commit("SET_ICON", value);
  },
  setManagers({ commit }, value) {
    commit("SET_MANAGERS", value);
  },
  setStatements({ commit }, value) {
    commit("SET_STATEMENTS", value);
  },
  setLoading({ commit }, value) {
    commit("SET_LOADING", value);
  },
  async createPortfolio({ getters, dispatch }) {
    dispatch("setLoading", "draft");
    const draft = getters.getProjectData;
    draft.organisation = 56;
    const parsed = apiWriteParser(
      draft,
      getters.getAllCountryAnswers,
      getters.getAllDonorsAnswers
    );
    const { data } = await this.$axios.post(
      `api/projects/draft/${draft.country_office}/`,
      parsed
    );
    dispatch("projects/addProjectToList", data, { root: true });
    await dispatch("saveTeamViewers", data.id);
    dispatch("setLoading", false);
    return data.id;
  }
};

export const mutations = {
  SET_NAME: (state, name) => {
    state.name = name;
  },
  SET_DESCRIPTION: (state, description) => {
    state.description = description;
  },
  SET_STATUS: (state, status) => {
    state.status = status;
  },
  SET_ICON: (state, icon) => {
    state.icon = icon;
  },
  SET_MANAGERS: (state, managers) => {
    state.managers = managers;
  },
  SET_STATEMENTS: (state, statements) => {
    state.statements = statements;
  },
  SET_LOADING: (state, loading) => {
    state.loading = loading;
  }
};
