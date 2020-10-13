<template>
  <section class="portfolio-area">
    <div class="content-area">
      <tabs :tabs="tabs" :tab="tab" @handleTab="setTab">
        <template slot="title">
          <nuxt-link
            :to="localePath({ name: 'organisation-portfolio-management' })"
          >
            <fa icon="angle-left" size="sm" />
            <translate>Back</translate>
          </nuxt-link>
          <h2 class="translate">
            <translate :parameters="{ name }">
              Edit `{name}` portfolio
            </translate>
          </h2>
        </template>
      </tabs>
      <div class="DashboardListView">
        <el-row>
          <table-top-actions />
        </el-row>
        <el-row>
          <main-table />
        </el-row>
      </div>
    </div>
    <aside class="filter-area">
      <advanced-search />
    </aside>
    <!-- dialogs -->
    <error />
  </section>
</template>

<script>
import AdvancedSearch from '@/components/search/AdvancedSearch'
import MainTable from '@/components/portfolio/dashboard/MainTable'
import TableTopActions from '@/components/portfolio/dashboard/TableTopActions'
import Tabs from '@/components/common/Tabs'
import { mapState, mapGetters, mapActions } from 'vuex'
import debounce from 'lodash/debounce'
// dialogs
import Error from '@/components/portfolio/dashboard/dialog/Error'

export default {
  components: {
    AdvancedSearch,
    MainTable,
    TableTopActions,
    Error,
    Tabs,
  },
  async fetch({ store, query, error, params }) {
    store.dispatch('landing/resetSearch')
    store.dispatch('dashboard/setDashboardSection', 'list')
    store.commit('portfolio/SET_VALUE', {
      key: 'currentPortfolioId',
      val: params.id,
    })
    store.commit('portfolio/SET_VALUE', {
      key: 'currentPortfolioId',
      val: params.id,
    })
    store.commit('search/SET_SEARCH', { key: 'portfolio', val: params.id })

    await Promise.all([
      store.dispatch('projects/loadUserProjects'),
      store.dispatch('projects/loadProjectStructure'),
      store.dispatch('portfolio/getPortfolioProjects'),
    ])
    await store.dispatch('dashboard/setSearchOptions', query)
    try {
      await store.dispatch('dashboard/loadProjectList')
    } catch (e) {
      console.log(e)
      error({
        statusCode: 404,
        message: 'Unable to process the search with the current parameters',
      })
    }
    // todo: integration should handle the status to refill data of initiatives
  },
  computed: {
    ...mapState({
      tabs: (state) => state.portfolio.tabs,
      tab: (state) => state.portfolio.tab,
      name: (state) => state.portfolio.name,
      errorDisplay: (state) => state.portfolio.errorDisplay,
      errorMessage: (state) => state.portfolio.errorMessage,
    }),
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
  mounted() {
    if (window) {
      const savedFilters = window.localStorage.getItem('savedFilters')
      if (savedFilters) {
        this.setSavedFilters(JSON.parse(savedFilters))
      }
    }
  },
  methods: {
    ...mapActions({
      loadProjectList: 'dashboard/loadProjectList',
      setSavedFilters: 'dashboard/setSavedFilters',
      setTab: 'portfolio/setTab',
    }),
    searchParameterChanged: debounce(function (query) {
      if (this.dashboardSection === 'list') {
        this.$router.replace({ ...this.$route, query })
        this.load()
      }
    }, 100),
    async load() {
      this.$nuxt.$loading.start()
      await this.loadProjectList()
      this.$nuxt.$loading.finish()
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.portfolio-area {
  height: calc(
    100vh - @topBarHeightSubpage - @actionBarHeight - @appFooterHeight
  );

  .content-area {
    overflow-y: scroll;
    .alert-portfolio {
      position: absolute;
      background-color: #fce9e8;
    }
  }
}
</style>
