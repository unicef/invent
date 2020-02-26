<template>
  <div class="DashboardListView">
    <el-row>
      <table-top-actions />
    </el-row>
    <el-row>
      <main-table />
    </el-row>
  </div>
</template>

<script>
import MainTable from '@/components/dashboard/MainTable';
import TableTopActions from '@/components/dashboard/TableTopActions';
import { mapGetters, mapActions } from 'vuex';
import debounce from 'lodash/debounce';

export default {
  components: {
    MainTable,
    TableTopActions
  },
  computed: {
    ...mapGetters({
      searchParameters: 'dashboard/getSearchParameters',
      dashboardSection: 'dashboard/getDashboardSection'
    })
  },
  watch: {
    searchParameters: {
      immediate: false,
      handler (query) {
        this.searchParameterChanged(query);
      }
    }
  },
  async fetch ({ store, query, error }) {
    store.dispatch('dashboard/setDashboardSection', 'list');
    await Promise.all([
      store.dispatch('projects/loadUserProjects'),
      store.dispatch('projects/loadProjectStructure'),
      store.dispatch('countries/loadMapData')
    ]);
    await store.dispatch('dashboard/setSearchOptions', query);
    try {
      await store.dispatch('dashboard/loadProjectList');
    } catch (e) {
      console.log(e);
      error({
        statusCode: 404,
        message: 'Unable to process the search with the current parameters'
      });
    }
    if (store.getters['dashboard/getDashboardType'] === 'donor') {
      await store.dispatch('system/loadDonorDetails', store.getters['dashboard/getDashboardId']);
    } else if (store.getters['dashboard/getDashboardType'] === 'country') {
      await store.dispatch('countries/loadCountryDetails', store.getters['dashboard/getDashboardId']);
    }
  },
  methods: {
    ...mapActions({
      loadProjectList: 'dashboard/loadProjectList'
    }),
    searchParameterChanged: debounce(function (query) {
      if (this.dashboardSection === 'list') {
        this.$router.replace({ ...this.$route, query });
        this.load();
      }
    }, 100),
    async load () {
      this.$nuxt.$loading.start();
      await this.loadProjectList();
      this.$nuxt.$loading.finish();
    }
  }
};
</script>

<style>

</style>
