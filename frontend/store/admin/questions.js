import { questionWriteParser } from '../../utilities/api'

export const state = () => ({
  questionnaireType: 'country',
  questions: [],
  reordered: false,
})

export const getters = {
  getQuestions: (state) => state.questions,
  getQuestionById: (state) => (id) => state.questions.find((q) => q.id === id),
  getReordered: (state) => state.reordered,
}

export const actions = {
  setQuestionnaireType({ commit }, type) {
    commit('SET_QUESTIONNAIRE_TYPE', type)
    commit('SET_QUESTIONS', [])
  },
  setQuestions({ commit, state }, data) {
    data = data[`${state.questionnaireType}_questions`]
    commit('SET_QUESTIONS', data)
  },

  addQuestion({ commit }) {
    commit('ADD_NEW_QUESTION')
  },

  async createQuestion({ state, rootGetters, commit }, question) {
    const type = state.questionnaireType
    const parent = rootGetters[`admin/${type}/getData`]
    const parsed = questionWriteParser(question, type, parent)
    const { data } = await this.$axios.post(
      `/api/${state.questionnaireType}-custom-questions/`,
      parsed
    )
    commit('UPDATE_QUESTION', { question: data, id: undefined })
  },

  async updateQuestion({ state, rootGetters, commit }, { question, id }) {
    const type = state.questionnaireType
    const parent = rootGetters[`admin/${type}/getData`]
    const parsed = questionWriteParser(question, type, parent)
    const { data } = await this.$axios.patch(
      `/api/${state.questionnaireType}-custom-questions/${id}/`,
      parsed
    )
    commit('UPDATE_QUESTION', { question: data, id })
  },

  async deleteQuestion({ commit, state }, id) {
    if (id) {
      await this.$axios.delete(
        `/api/${state.questionnaireType}-custom-questions/${id}/`
      )
    }
    commit('DELETE_QUESTION', id || undefined)
  },

  async processReOrder({ state, commit }, { from, to, newOrder }) {
    from = state.questions[from]
    to = state.questions[to]
    const {
      data,
    } = await this.$axios.post(
      `/api/${state.questionnaireType}-custom-questions/${from.id}/set_order_to/`,
      { to: to.order }
    )
    // positional order is important and should be respected, backend is sending ordered data so we use backend answer as base to map
    const mixed = data.map((d) => ({
      ...newOrder.find((n) => d.id === n.id),
      ...d,
    }))
    commit('SET_QUESTIONS', mixed)
  },
}

export const mutations = {
  SET_QUESTIONNAIRE_TYPE(state, type) {
    state.questionnaireType = type
  },
  SET_QUESTIONS(state, questions) {
    state.questions = [...questions]
  },
  ADD_NEW_QUESTION(state) {
    state.questions.push({})
  },
  UPDATE_QUESTION(state, { question, id }) {
    const index = state.questions.findIndex((q) => q.id === id)
    state.questions.splice(index, 1, question)
  },
  DELETE_QUESTION(state, id) {
    state.questions = state.questions.filter((q) => q.id !== id)
  },
}
