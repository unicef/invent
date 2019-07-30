import { stateGenerator, gettersGenerator, actionsGenerator, mutationsGenerator } from '../utilities/map';
import { intArrayFromQs, customColumnsMapper, strArrayFromQs, parseCustomAnswers } from '../utilities/api';

export const searchIn = () => ['name', 'org', 'overview', 'partner', 'donor', 'loc'];
export const defaultSelectedColumns = () => ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'];

export const state = () => ({
  ...stateGenerator(),
  searchIn: searchIn(),
  columns: [],
  selectedColumns: defaultSelectedColumns(),
  projectsList: [],
  projectsBucket: [],
  selectedDHI: [],
  selectedHFA: [],
  selectedHSC: [],
  selectedHIS: [],
  selectedPlatforms: [],
  selectedRows: [],
  filteredCountries: [],
  filteredOffice: null,
  filteredRegion: null,
  governmentApproved: null,
  governmentFinanced: null,
  selectAll: false,
  pageSize: 10,
  page: 1,
  total: 0,
  nextPage: 0,
  previousPage: 0,
  sorting: null,
  savedFilters: [],
  dashboardType: 'user',
  dashboardId: null,
  dashboardSection: 'map'
});
export const getters = {
  ...gettersGenerator(),
  getSearched: (state, getters) => {
    const g = getters.getSearchParameters;
    return !(g.approved === undefined &&
    g.country.length === 0 &&
    g.dhi.length === 0 &&
    g.donor === null &&
    g.gov === undefined &&
    g.hfa.length === 0 &&
    g.his.length === 0 &&
    g.hsc.length === 0 &&
    g.in === undefined &&
    g.q === undefined &&
    g.region === null &&
    g.sw.length === 0 &&
    g.view_as === undefined);
  },
  getProjectsList: state => [...state.projectsList.map(r => parseCustomAnswers(r))],
  getProjectsBucket: (state, getters) => state.selectAll ? [...state.projectsBucket.map(r => parseCustomAnswers(r))] : getters.getProjectsList,
  getCountryColumns: (state, getters, rootState, rootGetters) => {
    if (state.dashboardId && state.dashboardType === 'country') {
      const country = rootGetters['countries/getCountryDetails'](state.dashboardId);
      return country && country.country_questions ? customColumnsMapper(country.country_questions, 'c') : [];
    }
    return [];
  },
  getDonorColumns: (state, getters, rootState, rootGetters) => {
    if (state.dashboardId && state.dashboardType === 'donor') {
      const donor = rootGetters['system/getDonorDetails'](state.dashboardId);
      return donor && donor.donor_questions ? customColumnsMapper(donor.donor_questions, 'd') : [];
    }
    return [];
  },
  getAllColumns: (state, getters) => [...state.columns, ...getters.getCountryColumns, ...getters.getDonorColumns],
  getAvailableColumns: (state, getters) => [...getters.getAllColumns.map(c => ({ ...c, id: `${c.id}`, selected: state.selectedColumns.includes(`${c.id}`) }))],
  getSelectedColumns: state => state.selectedColumns.map(s => `${s}`),
  getSelectedDHI: state => state.selectedDHI,
  getSelectedHFA: state => state.selectedHFA,
  getSelectedHSC: state => state.selectedHSC,
  getSelectedHIS: state => state.selectedHIS,
  getSelectedPlatforms: state => state.selectedPlatforms,
  getSelectedRows: state => state.selectedRows,
  getFilteredCountries: state => {
    return state.dashboardType === 'country' && state.dashboardId ? [state.dashboardId] : state.filteredCountries;
  },
  getFilteredRegion: state => state.filteredRegion,
  getFilteredOffice: state => state.filteredOffice,
  getGovernmentApproved: state => state.governmentApproved,
  getGovernmentFinanced: state => state.governmentFinanced,
  getSelectAll: state => state.selectAll,
  getPageSize: state => state.pageSize,
  getTotal: state => state.total,
  getNextPage: state => state.nextPage,
  getPreviousPage: state => state.previousPage,
  getCurrentPage: state => state.page,
  getSorting: state => state.sorting,
  getSavedFilters: state => state.savedFilters,
  getDashboardType: state => state.dashboardType,
  getDashboardId: state => state.dashboardId,
  getDashboardSection: state => state.dashboardSection,
  getSearchParameters: (state, getters) => {
    const q = state.searchString && state.searchString.length > 1 ? state.searchString : undefined;
    const country = getters.getFilteredCountries;
    const donor = state.dashboardType === 'donor' ? [state.dashboardId] : null;
    return {
      page_size: state.pageSize,
      page: state.page,
      ordering: state.sorting,
      q,
      in: q ? state.searchIn : undefined,
      country,
      donor,
      region: state.filteredRegion,
      gov: state.governmentFinanced ? [1, 2] : undefined,
      approved: state.governmentApproved ? 1 : undefined,
      sw: state.selectedPlatforms,
      dhi: state.selectedDHI,
      hfa: state.selectedHFA,
      hsc: state.selectedHSC,
      his: state.selectedHIS,
      view_as: state.dashboardType !== 'user' ? state.dashboardType : undefined,
      sc: state.selectedColumns
    };
  }
};

export const actions = {
  ...actionsGenerator(),
  setDashboardColumns ({ commit }, columns) {
    commit('SET_DASHBOARD_COLUMNS', columns);
  },
  async loadProjectList ({ commit, dispatch }) {
    const data = await dispatch('loadProjects', { type: 'list' });
    commit('SET_PROJECT_LIST', data.results.projects);
    commit('SET_SEARCH_STATUS', data);
    commit('SET_SELECT_ALL', false);
    commit('SET_SELECTED_ROWS', []);
    commit('SET_PROJECT_BUCKET', []);
  },
  async loadProjectsMap ({ commit, dispatch }) {
    const data = await dispatch('loadProjects', { type: 'map', page_size: 999999, page: 1 });
    commit('SET_PROJECT_MAP', data.results.projects);
    commit('SET_SEARCH_STATUS', data);
  },
  async loadProjectsBucket ({ commit, dispatch, state }) {
    if (state.projectsBucket.length === 0) {
      const data = await dispatch('loadProjects', { type: 'list', page_size: 999999, page: 1 });
      commit('SET_PROJECT_BUCKET', data.results.projects);
      commit('SET_SEARCH_STATUS', data);
    }
  },
  async setSearchOptions ({ commit, dispatch }, options) {
    if (options.country && !Array.isArray(options.country)) {
      await dispatch('setSelectedCountry', +options.country);
      commit('SET_ACTIVE_COUNTRY', +options.country);
    }
    commit('SET_SEARCH_OPTIONS', options);
  },
  setSelectedColumns ({ commit }, columns) {
    commit('SET_SELECTED_COLUMNS', columns);
  },
  setSearchString ({ commit }, value) {
    commit('SET_SEARCH_STRING', value);
    commit('SET_CURRENT_PAGE', 1);
  },
  setSearchIn ({ commit }, value) {
    commit('SET_SEARCH_IN', value);
    commit('SET_CURRENT_PAGE', 1);
  },
  setSelectedDHI ({ commit }, columns) {
    commit('SET_SELECTED_DHI', columns);
    commit('SET_CURRENT_PAGE', 1);
  },
  setSelectedHFA ({ commit }, columns) {
    commit('SET_SELECTED_HFA', columns);
    commit('SET_CURRENT_PAGE', 1);
  },
  setSelectedHSC ({ commit }, columns) {
    commit('SET_SELECTED_HSC', columns);
    commit('SET_CURRENT_PAGE', 1);
  },
  setSelectedHIS ({ commit }, columns) {
    commit('SET_SELECTED_HIS', columns);
    commit('SET_CURRENT_PAGE', 1);
  },
  setSelectedPlatforms ({ commit }, columns) {
    commit('SET_SELECTED_PLATFORMS', columns);
    commit('SET_CURRENT_PAGE', 1);
  },
  setSelectedRows ({ commit, state }, rows) {
    if (state.selectAll && state.selectedRows.length > rows.length) {
      commit('SET_SELECT_ALL', false);
    }
    commit('SET_SELECTED_ROWS', rows);
  },
  async setFilteredCountries ({ commit, dispatch }, value) {
    if (value && value.length === 1) {
      await dispatch('setSelectedCountry', value[0]);
      commit('SET_ACTIVE_COUNTRY', value[0]);
    } else if (value && (value.length > 0 || value.length === 0)) {
      commit('SET_SELECTED_COUNTRY', null);
      commit('SET_ACTIVE_COUNTRY', null);
    }
    commit('SET_FILTERED_COUNTRIES', value);
    commit('SET_CURRENT_PAGE', 1);
  },
  setFilteredRegion ({ commit }, value) {
    commit('SET_FILTERED_REGION', value);
    commit('SET_CURRENT_PAGE', 1);
  },
  setFilteredOffice ({ commit }, value) {
    commit('SET_FILTERED_OFFICE', value);
    commit('SET_CURRENT_PAGE', 1);
  },
  setGovernmentApproved ({ commit }, value) {
    commit('SET_GOVERNMENT_APPROVED', value);
    commit('SET_CURRENT_PAGE', 1);
  },
  setGovernmentFinanced ({ commit }, value) {
    commit('SET_GOVERNMENT_FINANCED', value);
    commit('SET_CURRENT_PAGE', 1);
  },
  setSelectAll ({ commit }, all) {
    commit('SET_SELECT_ALL', all);
  },
  setPageSize ({ commit }, size) {
    commit('SET_PAGE_SIZE', size);
    commit('SET_CURRENT_PAGE', 1);
  },
  setCurrentPage ({ commit }, page) {
    commit('SET_CURRENT_PAGE', page);
  },
  setSorting ({ commit }, value) {
    commit('SET_SORTING', value);
    commit('SET_CURRENT_PAGE', 1);
  },
  setSavedFilters ({ commit }, filters) {
    if (window && window.localStorage) {
      window.localStorage.setItem('savedFilters', JSON.stringify(filters));
    }
    commit('SET_SAVED_FILTERS', filters);
  },
  async setDashboardType ({ commit, dispatch, getters }, { type, id }) {
    commit('SET_SEARCH_OPTIONS', {
      view_as: type,
      donor: type === 'donor' ? id : undefined,
      country: type === 'country' ? [id] : undefined
    });
    const selectedColumns = [...getters.getSelectedColumns];
    if (type === 'country') {
      selectedColumns.push(...getters.getCountryColumns.map(cc => cc.id));
      await dispatch('setSelectedCountry', id);
      commit('SET_ACTIVE_COUNTRY', id);
    } else if (type === 'donor') {
      selectedColumns.push(...getters.getDonorColumns.map(cc => cc.id));
    }
    commit('SET_PROJECT_BUCKET', []);
    commit('SET_SELECTED_COLUMNS', selectedColumns);
  },
  setDashboardSection ({ commit }, value) {
    commit('SET_DASHBOARD_SECTION', value);
  },
  resetUserInput ({ commit }) {
    commit('RESET_USER_INPUT');
    commit('SET_SEARCH_OPTIONS', {});
    commit('SET_SELECTED_COLUMNS', defaultSelectedColumns());
  }
};
export const mutations = {
  ...mutationsGenerator(),
  SET_DASHBOARD_COLUMNS: (state, columns) => {
    state.columns = columns;
  },
  SET_PROJECT_LIST: (state, projects) => {
    state.projectsList = projects;
  },
  SET_PROJECT_BUCKET: (state, projects) => {
    state.projectsBucket = projects;
  },
  SET_SEARCH_OPTIONS: (state, options) => {
    state.pageSize = options.page_size ? +options.page_size : 10;
    state.page = options.page ? +options.page : 1;
    state.sorting = options.ordering ? options.ordering : null;
    state.searchString = options.q ? options.q : '';
    state.searchIn = options.in ? options.in : searchIn();
    state.filteredCountries = intArrayFromQs(options.country);
    state.filteredRegion = options.region ? +options.region : null;
    state.governmentFinanced = options.gov ? true : null;
    state.governmentApproved = options.approved ? true : null;
    state.selectedPlatforms = intArrayFromQs(options.sw);
    state.selectedDHI = intArrayFromQs(options.dhi);
    state.selectedHFA = intArrayFromQs(options.hfa);
    state.selectedHSC = intArrayFromQs(options.hsc);
    state.selectedHIS = intArrayFromQs(options.his);
    state.selectedColumns = options.sc ? strArrayFromQs(options.sc) : defaultSelectedColumns();
    state.dashboardType = options.view_as ? options.view_as : 'user';
    state.dashboardId = options.view_as === 'country' ? intArrayFromQs(options.country)[0] : options.view_as === 'donor' ? +options.donor : null;
  },
  SET_SELECTED_COLUMNS: (state, columns) => {
    state.selectedColumns = columns;
  },
  SET_SELECTED_DHI: (state, dhi) => {
    state.selectedDHI = dhi;
  },
  SET_SELECTED_HFA: (state, hfa) => {
    state.selectedHFA = hfa;
  },
  SET_SELECTED_HSC: (state, hsc) => {
    state.selectedHSC = hsc;
  },
  SET_SELECTED_HIS: (state, his) => {
    state.selectedHIS = his;
  },
  SET_SELECTED_PLATFORMS: (state, platforms) => {
    state.selectedPlatforms = platforms;
  },
  SET_SELECTED_ROWS: (state, rows) => {
    state.selectedRows = rows;
  },
  SET_FILTERED_COUNTRIES: (state, value) => {
    state.filteredCountries = value;
  },
  SET_FILTERED_OFFICE: (state, value) => {
    state.filteredOffice = value;
  },
  SET_FILTERED_REGION: (state, value) => {
    state.filteredRegion = value;
  },
  SET_GOVERNMENT_APPROVED: (state, value) => {
    state.governmentApproved = value;
  },
  SET_GOVERNMENT_FINANCED: (state, value) => {
    state.governmentFinanced = value;
  },
  SET_SELECT_ALL: (state, all) => {
    state.selectAll = all;
  },
  SET_PAGE_SIZE: (state, size) => {
    state.pageSize = size;
  },
  SET_CURRENT_PAGE: (state, page) => {
    state.page = page;
  },
  SET_SORTING: (state, value) => {
    state.sorting = value;
  },
  SET_SEARCH_STATUS: (state, status) => {
    state.total = status.count;
    state.nextPage = status.next;
    state.previousPage = status.previous;
  },
  SET_SAVED_FILTERS: (state, filters) => {
    state.savedFilters = filters;
  },
  SET_DASHBOARD_TYPE: (state, { type, id }) => {
    state.dashboardType = type;
    state.dashboardId = id;
  },
  SET_DASHBOARD_SECTION: (state, section) => {
    state.dashboardSection = section;
  }
};
