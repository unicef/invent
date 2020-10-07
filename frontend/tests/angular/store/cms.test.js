import * as CmsModule from '../../../angular/store/modules/cms'
import { defaultAxiosSuccess, dispatch, getState } from '../testUtilities'

describe('CMS Store Module', () => {
  describe('GETTERS', () => {
    beforeEach(() => {
      window.$nuxt = {
        $store: {
          getters: {},
        },
        $axios: {
          get: () => {},
          post: () => {},
          put: () => {},
          patch: () => {},
          delete: () => {},
        },
      }
    })

    test('getCmsData', () => {
      const state = {
        cms: {
          data: [],
        },
      }
      const result = CmsModule.getters.getCmsData(state)
      expect(result).not.toBe(state.cms.data)
      expect(result).toEqual(state.cms.data)
    })

    test('getDomainStructureForCms', () => {
      window.$nuxt.$store.getters['system/getAxis'] = [{ id: 1 }]
      window.$nuxt.$store.getters['system/getDomains'] = [
        { id: 1, axis: 1, name: 1 },
      ]
      const result = CmsModule.getters.getDomainStructureForCms({})
      expect(result[0].id).toBe(1)
      expect(result[0].domains[0].name).toBe(1)
    })

    test('getAxisName', () => {
      window.$nuxt.$store.getters['system/getAxis'] = [{ id: 1, name: 'a' }]
      const result = CmsModule.getters.getAxisName({}, 0)
      expect(result).toBe('a')
    })

    test('getDomain', () => {
      window.$nuxt.$store.getters['system/getDomains'] = [
        { id: 1, axis: 1, name: 1 },
      ]
      const result = CmsModule.getters.getDomain({}, 1)
      expect(result.name).toBe(1)
    })

    test('getAxisAndDomainName', () => {
      jest
        .spyOn(CmsModule.getters, 'getDomain')
        .mockReturnValue({ name: 'domain', id: 1 })
      jest
        .spyOn(CmsModule.getters, 'getDomainStructureForCms')
        .mockReturnValue([
          { name: 'axis', domains: [{ id: 1 }] },
          { name: 'wrong', domains: [{ id: 2 }] },
        ])

      const result = CmsModule.getters.getAxisAndDomainName({}, 1)
      expect(result.axisName).toBe('axis')
      expect(result.domainName).toBe('domain')

      expect(CmsModule.getters.getDomain).toHaveBeenCalledWith({}, 1)
      expect(CmsModule.getters.getDomainStructureForCms).toHaveBeenCalled()
    })
  })

  describe('ACTIONS', () => {
    test('loadCmsData', async (done) => {
      jest
        .spyOn(window.$nuxt.$axios, 'get')
        .mockReturnValue(Promise.resolve({ data: [{}] }))
      await CmsModule.actions.loadCmsData()(dispatch)
      expect(window.$nuxt.$axios.get).toHaveBeenCalledWith('/api/cms/')
      expect(dispatch).toHaveBeenCalledWith({
        type: 'SET_CMS_DATA',
        data: [{ searchOccurrences: 0 }],
      })
      done()
    })

    test('addContent', async (done) => {
      jest
        .spyOn(window.$nuxt.$axios, 'post')
        .mockReturnValue(Promise.resolve({ data: {} }))
      await CmsModule.actions.addContent({ a: 1 })(dispatch)
      expect(window.$nuxt.$axios.post).toHaveBeenCalledWith('/api/cms/', {
        a: 1,
      })
      expect(dispatch).toHaveBeenCalledWith({
        type: 'ADD_CMS_ENTRY',
        item: { searchOccurrences: 0 },
      })
      done()
    })

    test('updateContent', async (done) => {
      jest
        .spyOn(window.$nuxt.$axios, 'put')
        .mockReturnValue(Promise.resolve({ data: {} }))
      await CmsModule.actions.updateContent({ a: 1 }, 1)(dispatch)
      expect(window.$nuxt.$axios.put).toHaveBeenCalledWith('/api/cms/1/', {
        a: 1,
      })
      expect(dispatch).toHaveBeenCalledWith({
        type: 'UPDATE_CMS_ENTRY',
        item: { searchOccurrences: 0 },
      })
      done()
    })

    test('saveOrUpdateContent', async (done) => {
      const state = getState({
        user: {
          profile: {
            id: 1,
          },
        },
      })

      jest.spyOn(CmsModule.actions, 'addContent')
      const update = jest.spyOn(CmsModule.actions, 'updateContent')
      window.$nuxt.$store.getters['user/getProfile'] = { id: 1 }
      const resource = {
        id: 1,
      }
      await CmsModule.actions.saveOrUpdateContent(resource)(dispatch, state)
      expect(CmsModule.actions.updateContent).toHaveBeenCalledWith(
        { id: 1, author: 1 },
        1
      )

      resource.cover = {
        type: ['asd'],
      }

      await CmsModule.actions.saveOrUpdateContent(resource)(dispatch, state)
      expect(CmsModule.actions.updateContent).toHaveBeenCalledWith(
        { id: 1, author: 1 },
        1
      )

      update.mockClear()
      resource.cover.type = ['image']
      await CmsModule.actions.saveOrUpdateContent(resource)(dispatch, state)
      expect(CmsModule.actions.updateContent).toHaveBeenCalledWith(
        expect.any(FormData),
        1
      )

      delete resource.id
      await CmsModule.actions.saveOrUpdateContent(resource)(dispatch, state)
      expect(CmsModule.actions.addContent).toHaveBeenCalledWith(
        expect.any(FormData)
      )
      done()
    })

    test('deleteContent', async (done) => {
      jest
        .spyOn(window.$nuxt.$axios, 'delete')
        .mockReturnValue(defaultAxiosSuccess)
      await CmsModule.actions.deleteContent({ id: 1 })(dispatch)
      expect(window.$nuxt.$axios.delete).toHaveBeenCalledWith('/api/cms/1/')
      expect(dispatch).toHaveBeenCalledWith({ type: 'DELETE_CMS_ENTRY', id: 1 })
      done()
    })

    test('reportContent', async (done) => {
      jest
        .spyOn(window.$nuxt.$axios, 'patch')
        .mockReturnValue(defaultAxiosSuccess)
      await CmsModule.actions.reportContent({ id: 1 })(dispatch)
      expect(window.$nuxt.$axios.patch).toHaveBeenCalledWith('/api/cms/1/')
      expect(dispatch).toHaveBeenCalledWith({
        type: 'UPDATE_CMS_ENTRY',
        item: { id: 1, state: 2 },
      })
      done()
    })

    test('reportComment', async (done) => {
      jest
        .spyOn(window.$nuxt.$axios, 'patch')
        .mockReturnValue(defaultAxiosSuccess)
      await CmsModule.actions.reportComment({ id: 1 })(dispatch)
      expect(window.$nuxt.$axios.patch).toHaveBeenCalledWith('/api/comment/1/')
      expect(dispatch).toHaveBeenCalledWith({
        type: 'UPDATE_COMMENT',
        comment: { id: 1, state: 2 },
      })
      done()
    })

    test('deleteComment', async (done) => {
      jest
        .spyOn(window.$nuxt.$axios, 'delete')
        .mockReturnValue(defaultAxiosSuccess)
      await CmsModule.actions.deleteComment({ id: 1 })(dispatch)
      expect(window.$nuxt.$axios.delete).toHaveBeenCalledWith('/api/comment/1/')
      expect(dispatch).toHaveBeenCalledWith({
        type: 'DELETE_COMMENT',
        comment: { id: 1 },
      })
      done()
    })

    test('addNewComment', async (done) => {
      jest
        .spyOn(window.$nuxt.$axios, 'post')
        .mockReturnValue(defaultAxiosSuccess)
      const state = getState({
        user: {
          profile: {
            id: 1,
          },
        },
      })
      await CmsModule.actions.addNewComment({}, { id: 1 })(dispatch, state)
      expect(window.$nuxt.$axios.post).toHaveBeenCalledWith('/api/comment/', {
        post: 1,
        user: 1,
      })
      expect(dispatch).toHaveBeenCalledWith({ type: 'ADD_COMMENT', comment: 1 })
      done()
    })

    test('updateComment', async (done) => {
      jest
        .spyOn(window.$nuxt.$axios, 'put')
        .mockReturnValue(defaultAxiosSuccess)
      await CmsModule.actions.updateComment({ id: 1 })(dispatch)
      expect(window.$nuxt.$axios.put).toHaveBeenCalledWith('/api/comment/1/', {
        id: 1,
      })
      expect(dispatch).toHaveBeenCalledWith({
        type: 'UPDATE_COMMENT',
        comment: 1,
      })
      done()
    })
  })

  describe('REDUCERS', () => {
    test('SET_CMS_DATA', () => {
      let state = {}
      const action = { type: 'SET_CMS_DATA', data: 1 }
      state = CmsModule.default(state, action)
      expect(state.data).toBe(1)
    })

    test('ADD_CMS_ENTRY', () => {
      let state = {
        data: [],
      }
      const action = { type: 'ADD_CMS_ENTRY', item: 1 }
      state = CmsModule.default(state, action)
      expect(state.data[0]).toBe(1)
    })

    test('UPDATE_CMS_ENTRY', () => {
      let state = {
        data: [{ id: 1, name: 3 }],
      }
      const action = { type: 'UPDATE_CMS_ENTRY', item: { id: 1, name: 2 } }
      state = CmsModule.default(state, action)
      expect(state.data[0].name).toBe(2)
    })

    test('DELETE_CMS_ENTRY', () => {
      let state = {
        data: [{ id: 1, name: 3 }],
      }
      const action = { type: 'DELETE_CMS_ENTRY', id: 1 }
      state = CmsModule.default(state, action)
      expect(state.data[0]).toEqual(undefined)
    })

    test('ADD_COMMENT', () => {
      let state = {
        data: [{ id: 1, comments: [] }],
      }
      const action = { type: 'ADD_COMMENT', comment: { post: 1, id: 2 } }
      state = CmsModule.default(state, action)
      expect(state.data[0].comments[0].id).toEqual(2)
    })

    test('UPDATE_COMMENT', () => {
      let state = {
        data: [{ id: 1, comments: [{ id: 2, post: 1, name: 3 }] }],
      }
      const action = {
        type: 'UPDATE_COMMENT',
        comment: { post: 1, id: 2, name: 4 },
      }
      state = CmsModule.default(state, action)
      expect(state.data[0].comments[0].name).toEqual(4)
    })

    test('DELETE_COMMENT', () => {
      let state = {
        data: [{ id: 1, comments: [{ id: 2, post: 1, name: 3 }] }],
      }
      const action = {
        type: 'DELETE_COMMENT',
        comment: { post: 1, id: 2, name: 4 },
      }
      state = CmsModule.default(state, action)
      expect(state.data[0].comments[0]).toEqual(undefined)
    })

    test('CLEAR_CMS_DATA', () => {
      let state = {
        data: [{ id: 1, comments: [{ id: 2, post: 1, name: 3 }] }],
      }
      const action = { type: 'CLEAR_CMS_DATA' }
      state = CmsModule.default(state, action)
      expect(state.data).toEqual([])
    })
    test('DEFAULT', () => {
      let state = 1
      state = CmsModule.default(state, '')
      expect(state).toEqual(1)
    })
  })
})
