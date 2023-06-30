import union from 'lodash/union'
import { saveToken, deleteToken } from '../utilities/auth'

export const state = () => ({
  token: null,
  user: null,
  profile: null,
  emailVerifyResult: null,
  feedbackOn: false,
  feedbackForm: {
    subject: '',
    message: '',
  },
})

export const getters = {
  getToken: (state) => state.token,
  getUser: (state) => state.user,
  emailVerifiedRecently: (state) => state.emailVerifyResult,

  getProfile: (state) => {
    if (state.profile) {
      return { ...state.profile }
    }
    return null
  },
  getAccountApproved: (state) => {
    return state.profile.account_type_approved
  },
}

export const actions = {
  async doLogin({ commit, dispatch }, { username, password, code }) {
    let result
    if (code) {
      result = await this.$axios.post('/api/rest-auth/azure/', { code })
    } else {
      result = await this.$axios.post('/api/api-token-auth/', {
        username,
        password,
      })
    }
    const { data } = result
    commit('SET_USER', data)
    commit('SET_TOKEN', data.token)
    saveToken(data.token, data.user_profile_id)
    await dispatch('loadProfile', data.user_profile_id)
    await Promise.all([
      dispatch('system/loadOrganisations', {}, { root: true }),
      dispatch('projects/loadUserProjects', {}, { root: true }),
      dispatch('system/loadUserProfiles', {}, { root: true }),
    ])
  },

  async resetPassword(ctx, { email }) {
    const { data } = await this.$axios.post('/api/rest-auth/password/reset/', {
      email,
    })
    return data
  },

  async doSignup({ commit, dispatch }, { account_type, password1, password2, email }) {
    const { data } = await this.$axios.post('/api/rest-auth/registration/', {
      account_type,
      password1,
      password2,
      email,
    })
    commit('SET_USER', data)
    commit('SET_TOKEN', data.token)
    saveToken(data.token, data.user_profile_id)
    await dispatch('loadProfile', data.user_profile_id)
    await dispatch('system/loadOrganisations', {}, { root: true })
  },

  async dorResetPassword({ commit, dispatch }, { token, password1, password2 }) {
    await this.$axios.post(
      '/api/rest-auth/password/reset-password', // TODO
      { token, password1, password2 }
    )
  },

  doLogout({ commit, dispatch }) {
    commit('SET_USER', null)
    commit('SET_PROFILE', null)
    commit('SET_TOKEN', null)
    dispatch('dashboard/resetUserInput', null, { root: true })
    dispatch('landing/resetUserInput', null, { root: true })
    dispatch('projects/resetProjectsData', null, { root: true })
    deleteToken()
  },

  async loadProfile({ state, commit, getters }, profileId) {
    if (state.profile && state.profile.id === profileId) return
    try {
      if (getters.getToken && !getters.getProfile) {
        const { data } = await this.$axios.get(`/api/userprofiles/${profileId}/`)
        commit('SET_PROFILE', data)
      }
    } catch (e) {
      console.error('user/loadProfile failed')
    }
  },

  async refreshProfile({ commit, getters }) {
    try {
      if (getters.getToken && getters.getProfile && getters.getProfile.id) {
        const { data } = await this.$axios.get(`/api/userprofiles/${getters.getProfile.id}/`)
        commit('SET_PROFILE', data)
      }
    } catch (e) {
      console.error('user/loadProfile failed', e)
    }
  },

  async updateUserProfile({ commit, dispatch }, profile) {
    if (isNaN(profile.organisation)) {
      const organisation = await dispatch('system/addOrganisation', profile.organisation, { root: true })
      profile.organisation = organisation.id
    }
    const { data } = await this.$axios.put(`/api/userprofiles/${profile.id}/`, profile)
    data.email = data.email || data.user_email
    commit('SET_PROFILE', data)
  },

  async setToken({ commit, dispatch }, tokens) {
    commit('SET_TOKEN', tokens.jwt)
    await dispatch('loadProfile', tokens.profileId)
  },

  updateTeamViewers({ commit, getters }, { team, viewers, id }) {
    const user = getters.getProfile.id
    const originalTeam = getters.getProfile.member
    const originalViewer = getters.getProfile.viewer
    const member = team.includes(user) ? union(originalTeam, [id]) : originalTeam.filter((o) => o !== id)
    const viewer = viewers.includes(user) ? union(originalViewer, [id]) : originalViewer.filter((o) => o !== id)
    commit('UPDATE_TEAM_VIEWER', { member, viewer })
    return team.includes(user) || viewers.includes(user)
  },

  async verifyEmail({ commit }, key) {
    try {
      await this.$axios.post('/api/rest-auth/registration/verify-email/', {
        key,
      })
      commit('EMAIL_VERIFY_RESULT', true)
    } catch (e) {
      commit('EMAIL_VERIFY_RESULT', false)
    }
  },
}

export const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },

  SET_USER: (state, user) => {
    state.user = user
  },

  SET_PROFILE: (state, profile) => {
    state.profile = profile
  },

  UPDATE_TEAM_VIEWER: (state, { member, viewer }) => {
    state.profile = { ...state.profile, member, viewer }
  },

  EMAIL_VERIFY_RESULT: (state, isSuccess) => {
    state.emailVerifyResult = isSuccess
  },

  SET_FEEDBACK: (state, { feedbackOn, feedbackForm }) => {
    state.feedbackOn = feedbackOn
    if (feedbackForm) {
      state.feedbackForm = Object.assign({}, state.feedbackForm, feedbackForm)
    }
  },
}
