import map from 'lodash/map'
import find from 'lodash/find'
import compact from 'lodash/compact'

export const state = () => ({
  ambitionMatrix: [],
  riskImpactMatrix: [],
  problemStatementMatrix: [],
})

export const actions = {
  setPortfolioMatrix({ commit }, data) {
    const {
      ambition_matrix,
      risk_impact_matrix,
      problem_statement_matrix,
    } = data
    commit('SET_VALUE', { key: 'ambitionMatrix', val: ambition_matrix })
    commit('SET_VALUE', { key: 'riskImpactMatrix', val: risk_impact_matrix })
    commit('SET_VALUE', {
      key: 'problemStatementMatrix',
      val: problem_statement_matrix,
    })
  },
}

function processMatrix(matrix, projects) {
  if (!projects || projects.length === 0) {
    return []
  }
  return map(matrix, function (element) {
    return {
      ...element,
      projects: compact(
        map(element.projects, function (projectId) {
          const project = find(projects, ({ id }) => id === projectId)
          if (!project) {
            return null
          }
          return {
            id: projectId,
            title: project.name,
          }
        })
      ),
    }
  })
}

export const getters = {
  getAmbitionMatrix(state, getters, rootState) {
    return processMatrix(state.ambitionMatrix, rootState.portfolio.projects)
  },
  getRiskImpactMatrix(state, getters, rootState) {
    return processMatrix(state.riskImpactMatrix, rootState.portfolio.projects)
  },
  getProblemStatementMatrix(state, getters, rootState) {
    const { problemStatements } = rootState.portfolio
    const { neglected, moderate, high_activity } = state.problemStatementMatrix
    return [
      processProblemStatement(neglected, problemStatements),
      processProblemStatement(moderate, problemStatements),
      processProblemStatement(high_activity, problemStatements),
    ]
  },
}

function processProblemStatement(list, statements) {
  return map(list, function (statementId) {
    const statement = find(statements, ({ id }) => id === statementId)
    return {
      id: statementId,
      title: statement && statement.name,
      description: statement && statement.description,
    }
  })
}

export const mutations = {
  SET_VALUE(state, { key, val }) {
    state[key] = val
  },
}
