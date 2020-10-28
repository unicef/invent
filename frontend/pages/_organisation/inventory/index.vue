<template>
  <div class="DashboardMapView">
    <dashboard-map />
    <dashboard-project-box />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import debounce from 'lodash/debounce'
import DashboardMap from '@/components/dashboard/DashboardMap'
import DashboardProjectBox from '@/components/dashboard/DashboardProjectBox'
export default {
  components: {
    DashboardMap,
    DashboardProjectBox,
  },
  async fetch({ store, query, error }) {
    store.dispatch('dashboard/setDashboardSection', 'map')
    await Promise.all([
      store.dispatch('projects/loadUserProjects'),
      store.dispatch('projects/loadProjectStructure'),
      store.dispatch('countries/loadMapData'),
    ])
    await store.dispatch('dashboard/setSearchOptions', query)
    try {
      await store.dispatch('dashboard/loadProjectsMap')
    } catch (e) {
      console.log(e)
      error({
        statusCode: 404,
        message: 'Unable to process the search with the current parameters',
      })
    }
  },
  computed: {
    ...mapGetters({
      searchParameters: 'dashboard/getSearchParameters',
      dashboardSection: 'dashboard/getDashboardSection',
    }),
  },
  watch: {
    searchParameters: {
      immediate: false,
      handler(query) {
        this.searchParameterChanged(query)
      },
    },
  },
  methods: {
    ...mapActions({
      loadProjectsMap: 'dashboard/loadProjectsMap',
    }),
    searchParameterChanged: debounce(function (query) {
      if (this.dashboardSection === 'map') {
        this.$router.replace({ ...this.$route, query })
        this.load()
      }
    }, 100),
    async load() {
      this.$nuxt.$loading.start()
      await this.loadProjectsMap()
      this.$nuxt.$loading.finish()
    },
  },
}
</script>

<style lang="less">
.DashboardMapView {
  position: relative;
}
</style>
