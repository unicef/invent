import cloneDeep from 'lodash/cloneDeep'

export const state = () => ({
  toolkitData: [],
})

export const getters = {
  getToolkitData: (state) => {
    const data = state.toolkitData
    return data ? cloneDeep(data) : []
  },
  getStructure: (state, getters, rootState, rootGetters) => {
    const axis = rootGetters['system/getAxis']
    const domains = rootGetters['system/getDomains']
    const questions = rootGetters['system/getQuestions']
    return axis.map((a) => ({
      ...a,
      domains: domains
        .filter((d) => d.axis === a.id)
        .map((df) => ({
          ...df,
          questions: questions
            .filter((q) => q.domain === df.id)
            .map((qf) => ({ ...qf, id: `${qf.domain}-${qf.question_id}` })),
        })),
    }))
  },
  getDomainStructure: (state, getters) => (axis, domain) => {
    const structure = getters.getStructure
    return structure && structure[axis] && structure[axis].domains[domain]
      ? structure[axis].domains[domain]
      : {}
  },
  getAxisDetail: (state, getters, rootState, rootGetters) => (axisId) => {
    const axisStructure = rootGetters['system/getAxis'].find(
      (a) => a.id === axisId
    )
    const systemDomains = rootGetters['system/getDomains']
    const axisData = getters.getToolkitData.find((a) => a.id === axisId)
    const domains = axisData
      ? axisData.domains.map((add, index) => ({
          ...add,
          ...systemDomains.find((d) => d.id === add.id),
          index,
        }))
      : []
    return {
      ...axisStructure,
      ...axisData,
      domains,
    }
  },
}

export const actions = {
  async loadToolkitData({ commit, rootState }) {
    try {
      const projectId = rootState.projects.currentProject
      if (projectId) {
        const { data } = await this.$axios.get(
          `/api/projects/${projectId}/toolkit/data/`
        )
        commit('SET_TOOLKIT_DATA', data)
      }
    } catch (e) {
      return Promise.reject(e)
    }
  },
  async saveAnswer({ commit, dispatch, rootState }, answer) {
    try {
      const projectId = rootState.projects.currentProject
      if (projectId) {
        const { data } = await this.$axios.post(
          `/api/projects/${projectId}/toolkit/score/`,
          answer
        )
        commit('UPDATE_TOOLKIT_DATA', data)
        dispatch('loadToolkitData')
      }
    } catch (e) {
      console.log(e)
      return Promise.reject(e)
    }
  },
}
// Reducers
export const mutations = {
  SET_TOOLKIT_DATA: (state, data) => {
    state.toolkitData = data
  },
  UPDATE_TOOLKIT_DATA: (state, data) => {
    state.toolkitData[data.axis].domains[data.domain].questions[
      data.question
    ].answers[data.answer] = data.value
  },
  CLEAR_TOOLKIT_DATA: (state) => {
    state.toolkitData = []
  },
}
