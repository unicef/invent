import { objectToQueryString } from '@/utilities/search'

export const state = () => ({
  filter: {
    // ** SEARCH PARAMETERS **
    q: '',
    in: ['name', 'org', 'country', 'overview', 'loc', 'partner', 'donor'],
    // ** FILTER PARAMETERS **
    // `country` eg: country=1&country=2
    // `sw` eg: sw=1&sw=2
    // `dhi` eg: dhi=1&dhi=2
    // `hfa` eg: hfa=1&hfa=2
    // `hsc` eg: hsc=1&hsc=2
    // `his` eg: his=1&his=2
    region: '',
    // `gov` gov=0 (for false), gov=1&gov=2 (for true values, since there's two types of true)
    // `donor` eg: donor=1&donor=2
    // `approved` eg: approved=0 (for not approved), approved=1 (for approved)
    partner: [],
    // ** UNICEF filters **
    co: [], // `co` UNICEF Office eg: co=1&co=2
    // `fo` Field Office in eg: fo=1&fo=2
    goal: [], // `goal` Goal Area in eg: goal=1&goal=2
    // `result` Result Area in eg: result=1&result=2
    // `cl` Capability Levels overlap eg: cl=1&cl=2
    // `cc` Capability Categories overlap eg: cc=1&cc=2
    // `cs` Capability Sucategories overlap eg: cs=1&cs=2
    ic: [], // `ic` Innovation Categories overlap eg: ic=1&ic=2
    sp: '', // `sp` Scale Phase in eg: sp=1
    ps: [], // `ps` Problem Statement in eg: ps=1
    portfolio: '',
    // ** FOUND IN FEATURE **
    // `found` include if present (defaults to exclude)
    // ** TYPE AND ORDERING **
    type: 'portfolio', // map | list | portfolio (defaults to map) [eg: type=map]
    // `ordering` project__name | organisation__name | country__name |
    //            project__data__government_investor | country__region |
    //            project__modified
    // ** PAGINATION **
    page: 1, // `page` 1...n | last (will show the last page no matter the number)
    page_size: 10, // `page_size` eg: 20
    // ** VIEW AS **
    // `view_as` donor | country
    // ** PORTFOLIO OPTIONS **
    portfolio_page: 'inventory', // `portfolio_page` inventory | review | portfolio (defaults to portfolio)
    // `scores`  include if present (defaults to exclude)
  },
})

export const actions = {
  saveAnswer({ state, commit, dispatch, rootState }, answer) {},
  async getSearch({ state, commit, dispatch }) {
    try {
      const query = objectToQueryString(state.filter)
      const {
        data: {
          count,
          results: {
            projects,
            ambition_matrix,
            risk_impact_matrix,
            problem_statement_matrix,
          },
        },
      } = await this.$axios.get(`api/search${query}`)

      dispatch(
        'matrixes/setPortfolioMatrix',
        { ambition_matrix, risk_impact_matrix, problem_statement_matrix },
        { root: true }
      )

      dispatch('portfolio/setProjects', { projects, count }, { root: true })
    } catch (e) {
      console.error('search failed')
    }
  },
  resetSearch({ commit }) {
    commit('SET_SEARCH', { key: 'q', val: '' })
    commit('SET_SEARCH', {
      key: 'in',
      val: ['name', 'org', 'country', 'overview', 'loc', 'partner', 'donor'],
    })
    commit('SET_SEARCH', { key: 'region', val: '' })
    commit('SET_SEARCH', { key: 'partner', val: [] })
    commit('SET_SEARCH', { key: 'co', val: [] })
    commit('SET_SEARCH', { key: 'goal', val: [] })
    commit('SET_SEARCH', { key: 'ic', val: [] })
    commit('SET_SEARCH', { key: 'type', val: 'portfolio' })
    commit('SET_SEARCH', { key: 'ps', val: [] })
    commit('SET_SEARCH', { key: 'sp', val: '' })
    commit('SET_SEARCH', { key: 'page', val: 1 })
    commit('SET_SEARCH', { key: 'page_size', val: 10 })
    // manual setup
    // commit('SET_SEARCH', { key: 'portfolio', val: '' })
    // commit('SET_SEARCH', { key: 'portfolio_page', val: 'inventory' })
  },
}
// Reducers
export const mutations = {
  SET_SEARCH(state, { key, val }) {
    state.filter[key] = val
  },
}
