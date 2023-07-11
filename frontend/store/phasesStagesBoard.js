export const state = () => ({
  sectorsSelected: [],
  sectorsShown: [],
})

export const getters = {
  getSelectedSectors: (state) => state.sectorsSelected,
  getShownSectors: (state) => state.sectorsShown,
}

export const actions = {
  initSectors({ commit, rootGetters }) {
    const sectors = rootGetters['projects/getSectors']
    const sectorsAllSelected = sectors.map((sector) => ({ ...sector, selected: true }))
    commit('SET_SECTORS_SELECTED', sectorsAllSelected)
    commit('SET_SECTORS_SHOWN', sectorsAllSelected)
  },
  updateSectors({ commit, getters }) {
    commit('SET_SECTORS_SHOWN', getters.getSelectedSectors)
  },
  invertSelectSector({ commit, getters }, sectorId) {
    const updatedSelectors = getters.getSelectedSectors.map((sector) =>
      sector.id === sectorId ? { ...sector, selected: !sector.selected } : sector
    )
    commit('SET_SECTORS_SELECTED', updatedSelectors)
  },

  deselectAll({ commit, getters }) {
    const deselectedSectors = getters.getSelectedSectors.map((sector) => ({ ...sector, selected: false }))
    commit('SET_SECTORS_SELECTED', deselectedSectors)
  },
  selectAll({ commit, getters }) {
    const deselectedSectors = getters.getSelectedSectors.map((sector) => ({ ...sector, selected: true }))
    commit('SET_SECTORS_SELECTED', deselectedSectors)
  },
}

export const mutations = {
  SET_SECTORS_SELECTED(state, sectors) {
    state.sectorsSelected = sectors
  },
  SET_SECTORS_SHOWN(state, sectors) {
    state.sectorsShown = sectors
  },
}
