import findIndex from 'lodash/findIndex'

const initialState = {
  data: [],
}

// GETTERS
export const getters = {
  getCmsData(state) {
    return [...state.cms.data]
  },
  getDomainStructureForCms(state) {
    const axes = window.$nuxt.$store.getters['system/getAxis']
    const domains = window.$nuxt.$store.getters['system/getDomains']
    return axes.map((a) => ({
      ...a,
      domains: domains.filter((d) => d.axis === a.id),
    }))
  },

  getAxisName(state, index) {
    const axes = window.$nuxt.$store.getters['system/getAxis']
    return axes[index].name
  },

  getDomain(state, id) {
    const domains = window.$nuxt.$store.getters['system/getDomains']
    return domains.find((domain) => {
      return domain.id === id
    })
  },

  getAxisAndDomainName(state, domainId) {
    const domain = getters.getDomain(state, domainId)
    const axes = getters.getDomainStructureForCms(state)
    const axis = axes.find((ax) => {
      return ax.domains.some((dom) => {
        return dom.id === domain.id
      })
    })
    return {
      axisName: axis.name,
      domainName: domain.name,
    }
  },
}

// ACTIONS
export const actions = {
  loadCmsData() {
    return async (dispatch) => {
      let { data } = await window.$nuxt.$axios.get('/api/cms/')
      data = data.map((d) => {
        d.searchOccurrences = 0
        return d
      })
      dispatch({ type: 'SET_CMS_DATA', data })
    }
  },

  addContent(resource) {
    return async (dispatch) => {
      const { data } = await window.$nuxt.$axios.post('/api/cms/', resource)
      data.searchOccurrences = 0
      dispatch({ type: 'ADD_CMS_ENTRY', item: data })
    }
  },

  updateContent(resource, id) {
    return async (dispatch) => {
      const { data } = await window.$nuxt.$axios.put(
        `/api/cms/${id}/`,
        resource
      )
      data.searchOccurrences = 0
      dispatch({ type: 'UPDATE_CMS_ENTRY', item: data })
    }
  },

  saveOrUpdateContent(resource) {
    return (dispatch) => {
      resource = { ...resource }
      const profile = window.$nuxt.$store.getters['user/getProfile']
      resource.author = profile.id
      const id = resource.id || false
      if (resource.cover && !resource.cover.type.includes('image')) {
        delete resource.cover
      }
      if (resource.cover) {
        const formData = new FormData()
        for (const key in resource) {
          formData.append(key, resource[key])
        }
        resource = formData
      }

      if (id) {
        dispatch(actions.updateContent(resource, id))
      } else {
        dispatch(actions.addContent(resource))
      }
    }
  },

  deleteContent({ id }) {
    return async (dispatch) => {
      await window.$nuxt.$axios.delete(`/api/cms/${id}/`)
      dispatch({ type: 'DELETE_CMS_ENTRY', id })
    }
  },

  reportContent(resource) {
    return async (dispatch) => {
      await window.$nuxt.$axios.patch(`/api/cms/${resource.id}/`)
      resource.state = 2
      dispatch({ type: 'UPDATE_CMS_ENTRY', item: resource })
    }
  },

  reportComment(resource) {
    return async (dispatch) => {
      await window.$nuxt.$axios.patch(`/api/comment/${resource.id}/`)
      resource.state = 2
      dispatch({ type: 'UPDATE_COMMENT', comment: resource })
    }
  },

  deleteComment(comment) {
    return async (dispatch) => {
      await window.$nuxt.$axios.delete(`/api/comment/${comment.id}/`)
      dispatch({ type: 'DELETE_COMMENT', comment })
    }
  },

  addNewComment(comment, { id }) {
    return async (dispatch) => {
      comment.post = id
      comment.user = window.$nuxt.$store.getters['user/getProfile'].id
      const { data } = await window.$nuxt.$axios.post('/api/comment/', comment)
      dispatch({ type: 'ADD_COMMENT', comment: data })
    }
  },

  updateComment(comment) {
    return async (dispatch) => {
      const { data } = await window.$nuxt.$axios.put(
        `/api/comment/${comment.id}/`,
        comment
      )
      dispatch({ type: 'UPDATE_COMMENT', comment: data })
    }
  },
}

// Reducers

export default function cms(state = initialState, action) {
  switch (action.type) {
    case 'SET_CMS_DATA': {
      return { ...state, data: action.data }
    }
    case 'ADD_CMS_ENTRY': {
      return { ...state, data: [...state.data, action.item] }
    }
    case 'UPDATE_CMS_ENTRY': {
      const current = [...state.data]
      const index = findIndex(current, (i) => i.id === action.item.id)
      current.splice(index, 1, action.item)
      return { ...state, data: current }
    }
    case 'DELETE_CMS_ENTRY': {
      const current = [...state.data]
      const index = findIndex(current, (i) => i.id === action.id)
      current.splice(index, 1)
      return { ...state, data: current }
    }
    case 'ADD_COMMENT': {
      const current = [...state.data]
      const index = findIndex(current, (i) => i.id === action.comment.post)
      const item = current[index]
      item.comments.push(action.comment)
      current.splice(index, 1, item)
      return { ...state, data: current }
    }
    case 'UPDATE_COMMENT': {
      const current = [...state.data]
      const index = findIndex(current, (i) => i.id === action.comment.post)
      const item = current[index]
      const commentIndex = findIndex(
        item.comments,
        (com) => com.id === action.comment.id
      )
      item.comments.splice(commentIndex, 1, action.comment)
      current.splice(index, 1, item)
      return { ...state, data: current }
    }
    case 'DELETE_COMMENT': {
      const current = [...state.data]
      const index = findIndex(current, (i) => i.id === action.comment.post)
      const item = current[index]
      const commentIndex = findIndex(
        item.comments,
        (com) => com.id === action.comment.id
      )
      item.comments.splice(commentIndex, 1)
      current.splice(index, 1, item)
      return { ...state, data: current }
    }
    case 'CLEAR_CMS_DATA': {
      return { ...initialState }
    }
    default: {
      return state
    }
  }
}
