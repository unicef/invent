import { Message } from 'element-ui'

// export const state = () => ({
//   id: Number // countryId || donorId
//   type: '', // 'country' || 'donor'
//   data: {},
//   editableData: {},
//   userSelection: [],
//   adminSelection: [],
//   superadminSelection: []
// });

export const getters = () => ({
  getStableData: (state) => state.data,
  getData: (state) => state.editableData,

  getCoverText: (state) => state.editableData && state.editableData.cover_text,
  getFooterTitle: (state) =>
    state.editableData && state.editableData.footer_title,
  getFooterText: (state) =>
    state.editableData && state.editableData.footer_text,
  getProjectApproval: (state) =>
    state.editableData && state.editableData.project_approval,

  getUserSelection: (state) => state.userSelection,
  getAdminSelection: (state) => state.adminSelection,
  getSuperadminSelection: (state) => state.superadminSelection,
})

export const actions = () => ({
  setId({ commit }, id) {
    commit('SET_ID', id)
  },

  async fetchData({ state, commit, rootGetters, dispatch }) {
    const type = state.type === 'country' ? 'countries' : 'donors'

    const superUserSpecifiedId = state.id
    const idFromProfile = rootGetters['user/getProfile'][state.type]
    const firstDonorId =
      rootGetters['system/getDonors'].length &&
      rootGetters['system/getDonors'][0].id // fallback for superuser w/o donor

    const id = superUserSpecifiedId || idFromProfile || firstDonorId
    if (!id) {
      return Promise.reject(
        new Error(
          'No donor found in the database to be loaded or modified, make one first!'
        )
      )
    }
    const { data } = await this.$axios.get(`/api/${type}/${id}/`)
    // console.log(`${state.type} DATA for #${id}`);
    // console.dir(data);
    commit('SET_DATA', data)
    commit('SET_EDITABLE_DATA', data)

    if (state.type === 'country' && Object.keys(data.map_data).length) {
      dispatch('admin/map/setFacilities', data.map_data.facilities, {
        root: true,
      })
      dispatch(
        'admin/map/setFirstSubLevel',
        data.map_data.first_sub_level.admin_level,
        { root: true }
      )
      dispatch(
        'admin/map/setFirstSubLevelType',
        data.map_data.first_sub_level.name,
        { root: true }
      )
      dispatch(
        'admin/map/setFirstSubLevelList',
        data.map_data.first_sub_level.elements,
        { root: true }
      )
      dispatch(
        'admin/map/setSecondSubLevel',
        data.map_data.second_sub_level.admin_level,
        { root: true }
      )
      dispatch(
        'admin/map/setSecondSubLevelType',
        data.map_data.second_sub_level.name,
        { root: true }
      )
      dispatch(
        'admin/map/setSecondSubLevelList',
        data.map_data.second_sub_level.elements,
        { root: true }
      )
      dispatch('admin/map/setCountryCenter', data.map_data.polylabel, {
        root: true,
      })
      dispatch(
        'admin/map/setSecondSubLevelSource',
        data.map_data.second_sub_level_source,
        { root: true }
      )
    }

    if (state.type === 'country') {
      await dispatch('admin/map/loadGeoJSON', null, { root: true })
      await dispatch('admin/approval/loadList', null, { root: true })
    }

    dispatch('admin/questions/setQuestions', data, { root: true })

    dispatch('mapAdminSelections', data)
  },

  mapAdminSelections({ state, commit, rootGetters }, data) {
    const profiles = rootGetters['system/getUserProfiles']
    const userId = rootGetters['user/getProfile'].id
    let defaultDisable = false

    const userIdMapping = (val) => {
      if (typeof val !== 'object') {
        // In case of `id`
        const profile = profiles.find((prof) => prof.id === val)
        const label = `${profile.name} <${profile.email}>`
        return {
          key: val,
          label,
          disabled: defaultDisable || val === userId,
        }
      } else {
        // In case of { id, name, email }
        return {
          key: val.id,
          label: `${val.name} <${val.email}>`,
          disabled: defaultDisable || val.id === userId,
        }
      }
    }

    commit(
      'SET_USER_SELECTION',
      [...(data.user_requests || []), ...(data.users || [])].map(userIdMapping)
    )
    commit(
      'SET_ADMIN_SELECTION',
      [...(data.admin_requests || []), ...(data.admins || [])].map(
        userIdMapping
      )
    )
    const lesserAdminStr = state.type === 'country' ? 'CA' : 'DA'
    defaultDisable =
      rootGetters['user/getProfile'].account_type === lesserAdminStr &&
      !rootGetters['user/getProfile'].is_superuser
    commit(
      'SET_SUPER_ADMIN_SELECTION',
      [...(data.super_admin_requests || []), ...(data.super_admins || [])].map(
        userIdMapping
      )
    )
  },

  async saveChanges({ state, dispatch }) {
    try {
      await Promise.all([
        dispatch('patchInfoAndArrays'),
        dispatch('patchImages'),
        dispatch('synchPartnerLogos'),
        state.type === 'country' ? dispatch('synchMapFile') : Promise.resolve(),
        state.type === 'country'
          ? dispatch('admin/map/saveMapData', {}, { root: true })
          : Promise.resolve(),
      ])
      await dispatch('fetchData')
      window.scrollTo(0, 0)
      Message({
        message: 'Data succesfully updated',
        type: 'success',
        showClose: true,
      })
    } catch (e) {
      console.error(e)
      Message({
        message: 'Data update error',
        type: 'error',
        showClose: true,
      })
    }
  },

  async patchInfoAndArrays({ state, getters, rootGetters }) {
    const userProfile = rootGetters['user/getProfile']
    const keys = [
      'cover_text',
      'footer_title',
      'footer_text',
      'project_approval',
      'users',
      'admins',
    ]
    const superUserStr = state.type === 'country' ? 'SCA' : 'SDA'
    if (userProfile.account_type === superUserStr || userProfile.is_superuser)
      keys.push('super_admins')

    const patchObj = keys.reduce((prev, key) => {
      if (
        JSON.stringify(getters.getData[key]) !==
        JSON.stringify(getters.getStableData[key])
      ) {
        prev[key] = getters.getData[key]
      }
      return prev
    }, {})

    if (Object.keys(patchObj).length) {
      const type = state.type === 'country' ? 'countries' : 'donors'
      const id = state.id || rootGetters['user/getProfile'][state.type]
      await this.$axios.patch(`/api/${type}/${id}/`, patchObj)
    } else return Promise.resolve()
  },

  async patchImages({ state, getters, rootGetters }) {
    const oldFilePathLogo = getters.getStableData.logo
    const oldFilePathCover = getters.getStableData.cover

    const uploadNewLogo =
      oldFilePathLogo === null &&
      getters.getData.logo &&
      getters.getData.logo.raw
    const changeOldLogo =
      !!oldFilePathLogo && typeof getters.getData.logo !== 'string'
    const uploadNewCover =
      oldFilePathCover === null &&
      getters.getData.cover &&
      getters.getData.cover.raw
    const changeOldCover =
      !!oldFilePathCover && typeof getters.getData.cover !== 'string'

    const formData = new FormData()
    if (uploadNewLogo || changeOldLogo || uploadNewCover || changeOldCover) {
      const id = state.id || rootGetters['user/getProfile'][state.type]
      if (uploadNewLogo || changeOldLogo) {
        formData.append(
          'logo',
          (getters.getData.logo || '') && getters.getData.logo.raw
        )
      }
      if (uploadNewCover || changeOldCover) {
        formData.append(
          'cover',
          (getters.getData.cover || '') && getters.getData.cover.raw
        )
      }

      await this.$axios.patch(`/api/${state.type}-images/${id}/`, formData, {
        headers: {
          'content-type': 'multipart/form-data',
        },
      })
    } else {
      return Promise.resolve()
    }
  },

  synchPartnerLogos({ getters, dispatch }) {
    const promArr = []

    ;(getters.getData.partner_logos || []).forEach((logo) => {
      if (logo.raw) {
        promArr.push({ action: 'postPartnerLogo', data: { img: logo.raw } })
      }
    })
    ;(getters.getStableData.partner_logos || []).forEach((logo) => {
      const isStillThere = !!getters.getData.partner_logos.find(
        (newLogo) => newLogo.id === logo.id
      )
      if (!isStillThere) {
        promArr.push({ action: 'delPartnerLogo', data: { id: logo.id } })
      }
    })

    return Promise.all(
      promArr.map((promObj) => dispatch(promObj.action, promObj.data))
    )
  },

  async postPartnerLogo({ state, rootGetters }, { img }) {
    const id = state.id || rootGetters['user/getProfile'][state.type]
    const formData = new FormData()
    formData.append(state.type, id)
    formData.append('image', img)
    await this.$axios.post(`/api/${state.type}-partner-logos/`, formData, {
      headers: {
        'content-type': 'multipart/form-data',
      },
    })
  },

  async delPartnerLogo({ state }, { id }) {
    await this.$axios.delete(`/api/${state.type}-partner-logos/${id}/`)
  },

  setDataField({ commit }, { field, data }) {
    commit('SET_DATA_FIELD', { field, data })
  },

  setCoverText({ commit }, txt) {
    commit('SET_DATA_FIELD', { field: 'cover_text', data: txt })
  },

  setFooterTitle({ commit }, txt) {
    commit('SET_DATA_FIELD', { field: 'footer_title', data: txt })
  },

  setFooterText({ commit }, txt) {
    commit('SET_DATA_FIELD', { field: 'footer_text', data: txt })
  },
  setProjectApproval({ commit }, data) {
    commit('SET_DATA_FIELD', { field: 'project_approval', data })
  },
})

export const mutations = () => ({
  SET_ID: (state, id) => {
    state.id = id
  },

  SET_DATA: (state, data) => {
    state.data = { ...data }
  },

  SET_EDITABLE_DATA: (state, data) => {
    state.editableData = { ...data }
  },

  SET_DATA_FIELD: (state, { field, data }) => {
    const valueToFill = typeof data === 'undefined' ? null : data
    state.editableData[field] = valueToFill
  },

  SET_USER_SELECTION: (state, data) => {
    state.userSelection = data
  },

  SET_ADMIN_SELECTION: (state, data) => {
    state.adminSelection = data
  },

  SET_SUPER_ADMIN_SELECTION: (state, data) => {
    state.superadminSelection = data
  },
})
