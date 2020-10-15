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
// import debounce from 'lodash/debounce'
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
    // search setup
    store.dispatch('search/resetSearch')
    store.commit('search/SET_SEARCH', { key: 'portfolio', val: params.id })
    // project list setup and filters
    store.commit('portfolio/SET_VALUE', {
      key: 'currentPortfolioId',
      val: params.id,
    })
    // actual search
    await Promise.all([
      store.dispatch('projects/loadProjectStructure'),
      store.dispatch('portfolio/getPortfolioProjects'),
    ])
  },
  computed: {
    ...mapState({
      tabs: (state) => state.portfolio.tabs,
      tab: (state) => state.portfolio.tab,
      name: (state) => state.portfolio.name,
      errorDisplay: (state) => state.portfolio.errorDisplay,
      errorMessage: (state) => state.portfolio.errorMessage,
    }),
    ...mapGetters({}),
  },
  watch: {},
  mounted() {},
  methods: {
    ...mapActions({
      setTab: 'portfolio/setTab',
    }),
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
