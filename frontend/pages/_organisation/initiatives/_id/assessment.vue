<template>
  <div class="angularjs">
    <div id="assessmentjs" />
  </div>
</template>

<script>
import { fetchProjectData } from '@/utilities/projects'
export default {
  components: {},
  async fetch({ store, params, error }) {
    store.dispatch('landing/resetSearch')
    try {
      await fetchProjectData(store, params, error)
    } catch (e) {
      return
    }
    try {
      await store.dispatch('toolkit/loadToolkitData')
      const project = store.getters['projects/getCurrentProject']
      const country =
        project.published && project.published.country
          ? project.published.country
          : project.draft.country
      await store.dispatch('countries/loadMapData')
      await store.dispatch('countries/loadGeoJSON', country)
    } catch (e) {
      console.log('Error in assesment fetch', e)
      error({
        response: {
          status: 500,
          statusText: 'Server error',
        },
      })
    }
  },
  mounted() {
    const assesmentFactory = require('../../../../angular/Assessment/assessmentFactory')
    assesmentFactory.assesmentFactory()
  },
}
</script>

<style></style>
