import * as sharedStoreModule from '../../utilities/CountryDonorSharedStore.js'

export const state = () => ({
  id: null,
  type: 'donor',
  data: {},
  editableData: {},
  userSelection: [],
  adminSelection: [],
  superadminSelection: [],
})

export const getters = {
  ...sharedStoreModule.getters(),
}

export const actions = {
  ...sharedStoreModule.actions(),
}

export const mutations = {
  ...sharedStoreModule.mutations(),
}
