import Vue from "vue";
import get from "lodash/get";
import { apiReadParser, apiWriteParser, APIError } from "../utilities/api";

export const state = () => ({
  loading: false,
  name: "",
  description: "",
  status: "DR",
  icon: null,
  managers: [],
  statements: [],
  // portfolio icon set metadata
  icons: [
    { id: "1", title: "education", icon: "education" },
    { id: "2", title: "nutrition", icon: "nutrition" },
    { id: "3", title: "health", icon: "health" },
    { id: "4", title: "child_protection", icon: "child_protection" },
    { id: "5", title: "wash", icon: "wash" },
    { id: "6", title: "aids", icon: "aids" },
    { id: "7", title: "social_inclusion", icon: "social_inclusion" },
    { id: "8", title: "food_health", icon: "food_health" },
    { id: "9", title: "affected_population", icon: "affected_population" },
    { id: "10", title: "children", icon: "children" },
    { id: "11", title: "gender_balance", icon: "gender_balance" },
    { id: "14", title: "infant", icon: "infant" },
    { id: "15", title: "breast_feeding", icon: "breast_feeding" },
    {
      id: "16",
      title: "children_with_disabilities",
      icon: "children_with_disabilities"
    },
    { id: "27", title: "pregnant", icon: "pregnant" },
    { id: "29", title: "mental_health", icon: "mental_health" },
    { id: "30", title: "mother_and_baby", icon: "mother_and_baby" },
    { id: "34", title: "5year_old_girl", icon: "5year_old_girl" },
    { id: "38", title: "conflict", icon: "conflict" },
    { id: "42", title: "tsunami", icon: "tsunami" },
    { id: "45", title: "epidemic", icon: "epidemic" },
    { id: "52", title: "tent", icon: "tent" },
    { id: "69", title: "medical_supplies", icon: "medical_supplies" },
    { id: "70", title: "vaccines", icon: "vaccines" },
    { id: "71", title: "psychosocial_support", icon: "psychosocial_support" },
    { id: "72", title: "headquarters", icon: "headquarters" },
    { id: "73", title: "regional_office", icon: "regional_office" },
    { id: "92", title: "partnership", icon: "partnership" },
    { id: "97", title: "advocacy", icon: "advocacy" },
    { id: "113", title: "innovation", icon: "innovation" },
    { id: "116", title: "community_building", icon: "community_building" },
    { id: "164", title: "emergency", icon: "emergency" }
  ],
  statusList: [
    { id: "ACT", name: "Active" },
    { id: "DR", name: "Draft" },
    { id: "ARC", name: "Archived" }
  ],
  portfolios: [],
  portfolio: {},
  // dashboard of portfolio manager
  tabs: [
    { id: 1, name: "Inventory", icon: "folder", total: 46 },
    { id: 2, name: "For review", icon: "eye", total: 18 },
    { id: 3, name: "Portfolio", icon: "briefcase", total: 35 }
  ],
  tab: 1
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
  setTab({ commit }, val) {
    commit("SET_TAB", val);
  },
  async createPortfolio({ state, getters, dispatch }) {
    dispatch("setLoading", "create");
    const { data } = await this.$axios.post(`/api/portfolio/create/`, {
      name: state.name,
      description: state.description,
      status: state.status,
      icon: state.icon.id,
      managers: state.managers,
      problem_statements: state.statements.filter(i => i.name !== "")
    });
    dispatch("setLoading", false);
  },
  async editPortfolio({ state, getters, dispatch }, id) {
    dispatch("setLoading", "edit");
    const { data } = await this.$axios.patch(`/api/portfolio/update/${id}/`, {
      name: state.name,
      description: state.description,
      status: state.status,
      icon: state.icon.id,
      managers: state.managers,
      problem_statements: state.statements.filter(i => i.name !== "")
    });
    dispatch("setLoading", false);
  },
  async getPortfolios({ state, commit, dispatch }) {
    const { data } = await this.$axios.get("api/portfolio/manager-of/");
    const portfolios = data.map(i => {
      const icon = state.icons.find(item => item.id === i.icon).icon;
      return {
        id: i.id,
        name: i.name,
        total: i.project_count,
        status: status(i.status),
        icon
      };
    });
    commit("SET_PORTFOLIOS", portfolios);
  },
  async getPortfolioDetails({ state, commit, dispatch }, id) {
    const { data } = await this.$axios.get(`api/portfolio/${id}/`);
    commit("SET_NAME", data.name);
    commit("SET_DESCRIPTION", data.description);
    commit("SET_STATUS", data.status);
    commit("SET_ICON", state.icons.find(item => item.id === data.icon));
    commit("SET_MANAGERS", data.managers);
    commit("SET_STATEMENTS", data.problem_statements);
  },
  async resetPortfolio({ commit }) {
    commit("SET_NAME", "");
    commit("SET_DESCRIPTION", "");
    commit("SET_STATUS", "DR");
    commit("SET_ICON", null);
    commit("SET_MANAGERS", []);
    commit("SET_STATEMENTS", []);
  }
};

const status = status => {
  switch (status) {
    case "ACT":
      return "active";
    case "DR":
      return "draft";
    case "ARC":
      return "archived";
    default:
      break;
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
  },
  SET_PORTFOLIOS: (state, portfolios) => {
    state.portfolios = portfolios;
  },
  SET_PORTFOLIO: (state, portfolio) => {
    state.portfolio = portfolio;
  },
  SET_TAB: (state, tab) => {
    state.tab = tab;
  }
};
