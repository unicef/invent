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
  statements: [],
  // portfolio icon set metadata
  icons: [
    { id: 1, title: "education", icon: "education" },
    { id: 2, title: "nutrition", icon: "nutrition" },
    { id: 3, title: "health", icon: "health" },
    { id: 4, title: "child_protection", icon: "child_protection" },
    { id: 5, title: "wash", icon: "wash" },
    { id: 6, title: "aids", icon: "aids" },
    { id: 7, title: "social_inclusion", icon: "social_inclusion" },
    { id: 8, title: "food_health", icon: "food_health" },
    { id: 9, title: "affected_population", icon: "affected_population" },
    { id: 10, title: "children", icon: "children" },
    { id: 11, title: "gender_balance", icon: "gender_balance" },
    { id: 14, title: "infant", icon: "infant" },
    { id: 15, title: "breast_feeding", icon: "breast_feeding" },
    {
      id: 16,
      title: "children_with_disabilities",
      icon: "children_with_disabilities"
    },
    { id: 27, title: "pregnant", icon: "pregnant" },
    { id: 29, title: "mental_health", icon: "mental_health" },
    { id: 30, title: "mother_and_baby", icon: "mother_and_baby" },
    { id: 34, title: "5year_old_girl", icon: "5year_old_girl" },
    { id: 38, title: "conflict", icon: "conflict" },
    { id: 42, title: "tsunami", icon: "tsunami" },
    { id: 45, title: "epidemic", icon: "epidemic" },
    { id: 52, title: "tent", icon: "tent" },
    { id: 69, title: "medical_supplies", icon: "medical_supplies" },
    { id: 70, title: "vaccines", icon: "vaccines" },
    { id: 71, title: "psychosocial_support", icon: "psychosocial_support" },
    { id: 72, title: "headquarters", icon: "headquarters" },
    { id: 73, title: "regional_office", icon: "regional_office" },
    { id: 92, title: "partnership", icon: "partnership" },
    { id: 97, title: "advocacy", icon: "advocacy" },
    { id: 113, title: "innovation", icon: "innovation" },
    { id: 116, title: "community_building", icon: "community_building" },
    { id: 164, title: "emergency", icon: "emergency" }
  ],
  // example select
  managerList: [
    { id: 1, name: "Alonso" },
    { id: 2, name: "Torben" },
    { id: 3, name: "Gyuri" },
    { id: 4, name: "Daniel" },
    { id: 5, name: "David" }
  ],
  statusList: [
    { id: 1, name: "Active" },
    { id: 2, name: "On hold" },
    { id: 3, name: "Waiting" },
    { id: 4, name: "Cancel" }
  ]
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
  setStatus({ commit }, value) {
    commit("SET_STATUS", value);
  },
  setIcon({ commit }, value) {
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
