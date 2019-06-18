import * as sharedStoreModule from '../../utilities/CountryDonorSharedStore.js';

export const state = () => ({
  id: null,
  type: 'country',
  data: {},
  editableData: {},
  userSelection: [],
  adminSelection: [],
  superadminSelection: []
});

export const getters = {
  ...sharedStoreModule.getters()
};

export const actions = {
  ...sharedStoreModule.actions(),

  async synchMapFile ({ state, rootGetters, getters }) {
    const mapFile = getters.getData.map_files[0];
    if (mapFile && mapFile.raw) {
      const countryId = state.id || rootGetters['user/getProfile'].country;
      const formData = new FormData();
      formData.append('country', countryId);
      formData.append('map_file', mapFile.raw);
      await this.$axios.post(`/api/map-files/`, formData, {
        headers: {
          'content-type': 'multipart/form-data'
        }
      });
    }
  }
};

export const mutations = {
  ...sharedStoreModule.mutations()
};
