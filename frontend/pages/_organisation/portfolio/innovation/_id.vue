<template>
  <section class="portfolio-area">
    <div class="content-area-full">
      <div class="portfolio">
        <!-- tabs -->
        <tabs :tabs="tabs" :tab="tab" :center="false" @handleTab="setTab">
          <template slot="title">
            <div class="PHeader">
              <h2>
                <translate>Portfolio</translate>:
                <el-dropdown trigger="click" placement="bottom-start" @command="navigate">
                  <span class="Title el-dropdown-link">
                    {{ name }} <i class="el-icon-caret-bottom el-icon--right" />
                  </span>
                  <el-dropdown-menu slot="dropdown" class="PDropdown">
                    <el-dropdown-item v-for="portfolio in portfolios" :key="portfolio.id" :command="portfolio.id">
                      {{ portfolio.name }}
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </h2>
            </div>
          </template>
        </tabs>
        <section class="tab-content">
          <div v-if="tab === 1" class="Problems problem-matrix">
            <h1 class="portfolio-summary"><Translate>Summary</Translate></h1>
            <p>{{ description }}</p>
          </div>
        </section>
        <!-- tabs -->
        <div class="DashboardListView">
          <!-- <el-row>
            <table-top-actions />
          </el-row> -->
          <el-row>
            <main-solutions-table />
          </el-row>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import MainSolutionsTable from '@/components/solution/dashboard/MainSolutionsTable'
import Tabs from '@/components/common/Tabs'

import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  components: {
    MainSolutionsTable,
    Tabs,
  },
  data() {
    return {
      activeName: 'ambition',
      disabledProblems: [],

      // tabs information handle
      tabs: [
        {
          id: 1,
          name: this.$gettext('Summary'),
          icon: 'braille',
        },
        // {
        //   id: 2,
        //   name: this.$gettext('problem statement matrix'),
        //   icon: 'th',
        // },
        // {
        //   id: 3,
        //   name: this.$gettext('map view'),
        //   icon: 'columns',
        // },
      ],
      tab: 1,
    }
  },
  async fetch({ store, query, error, params }) {
    // setup search
    store.dispatch('search/resetSearch')
    store.dispatch('landing/resetSearch')
    store.dispatch('dashboard/setSearchOptions', query)
    // search setup
    store.commit('search/SET_SEARCH', {
      key: 'portfolio',
      val: params.id,
    })
    store.commit('search/SET_SEARCH', {
      key: 'portfolio_page',
      val: 'portfolio',
    })
    store.commit('search/SET_SEARCH', { key: 'scores', val: true })
    await Promise.all([
      store.dispatch('portfolio/getPortfolios', 'active-list'),
      store.dispatch('portfolio/getPortfolioDetails', {
        id: params.id,
        type: 'active-list',
      }),
    ])
  },
  computed: {
    ...mapState({
      ps: (state) => state.search.filter.ps,
      portfolios: (state) => state.portfolio.portfolios,
    }),
    ...mapGetters({
      name: 'portfolio/getName',
      description: 'portfolio/getDescription',
      selectedColumns: 'dashboard/getSelectedColumns',
    }),
  },
  mounted() {
    this.getSearch()
    this.setSelectedColumns(this.selectedColumns.filter((s) => s !== '61' && s !== '62'))
  },
  methods: {
    ...mapActions({
      loadProjectsMap: 'search/loadProjectsMap',
      getSearch: 'search/getSearch',
      setSelectedColumns: 'dashboard/setSelectedColumns',
    }),
    navigate(id) {
      this.$store.dispatch('search/resetSearch')
      this.$refs.ambitionMatrix.clear()
      this.$refs.riskMatrix.clear()
      this.$router.push(
        this.localePath({
          name: 'organisation-portfolio-innovation-id',
          params: { organisation: '-', id },
        })
      )
    },
    select(val, event) {
      if (event) {
        this.$store.commit('search/SET_SEARCH', { key: 'ps', val })
      } else {
        this.$store.commit('search/SET_SEARCH', { key: 'ps', val: '' })
      }
      this.getSearch()
    },
    setTab(id) {
      this.tab = id
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.tab-content {
  padding: 40px;
  background-color: #fbfaf8;
}
.portfolio-summary {
  font-size: @fontSizeHeading;
}
.portfolio-area::v-deep {
  .move {
    display: none;
  }
  .actions .right .settings {
    margin: 0;
  }
}
section.portfolio-area {
  aside.filter-area {
    right: 0;
    position: absolute;
  }
}
.portfolio {
  margin-bottom: 80px;
  .PHeader {
    background-color: white;
  }

  span.Title {
    display: inline-block;
    cursor: pointer;
    font-size: 36px;
    color: #1cabe2;
    &:focus {
      outline: none;
    }
  }
  h2 {
    margin: 0;
    height: 45px;
    color: #1cabe2;
    font-size: 36px;
    letter-spacing: -1px;
    line-height: 45px;
    font-weight: normal;
    .el-icon-caret-bottom {
      font-size: 22px;
    }
  }
  .map {
    position: relative;
  }
  .Problems {
    background-color: white;
    &.problem-matrix {
      background-color: transparent;
    }
    .Info {
      color: #777779;
      font-size: 12px;
      letter-spacing: 0;
      line-height: 15px;
      padding: 16px;
      .fa-info-circle {
        margin-right: 3px;
        font-size: 14px;
        color: #a8a8a9;
      }
    }
    .Problem {
      height: 100%;
      min-height: 560px;
      &.Problem1 {
        background-color: #cdedf9;
        margin-right: 7px;
      }
      &.Problem2 {
        background-color: #ade1f5;
        margin-right: 3px;
        margin-left: 3px;
      }
      &.Problem3 {
        margin-left: 7px;
        background-color: #7bcfef;
      }
      & > .Title {
        color: #404041;
        font-size: 18px;
        font-weight: bold;
        letter-spacing: -0.25px;
        line-height: 23px;
        text-align: center;
        padding: 29px 0;
        margin: 0;
      }
    }
  }
}
</style>
