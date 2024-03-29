<template>
  <section class="portfolio-area">
    <div class="content-area-full">
      <div class="portfolio">
        <!-- tabs -->
        <tabs-portfolios :tabs="tabs" :tab="tab" :center="false" @handleTab="setTab">
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
          <template slot="actionButton">
            <div class="SolutionsButton" v-show="canEdit">
              <nuxt-link
                :to="
                  localePath({
                    name: 'organisation-portfolio-management-id-edit',
                    params: { id: this.$route.params.id },
                  })
                "
              >
                <translate>Edit Portfolio</translate>
              </nuxt-link>
            </div>
          </template>
        </tabs-portfolios>
        <section class="tab-content">
          <div v-if="tab === 1" class="Problems problem-matrix">
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
import TabsPortfolios from '@/components/common/TabsPortfolios'

import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  components: {
    MainSolutionsTable,
    TabsPortfolios,
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
    await store.dispatch('solutions/loadSolutionsList', params.id)
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
      profile: 'user/getProfile',
    }),
    canEdit() {
      return (
        this.profile.is_superuser ||
        this.profile.global_portfolio_owner ||
        this.profile.manager.includes(this.$route.params.id * 1)
      )
    },
  },
  methods: {
    ...mapActions({
      loadProjectsMap: 'search/loadProjectsMap',
    }),
    navigate(id) {
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
  .SolutionsButton {
    width: 240px;
    display: flex;
    align-items: flex-end;
    color: @colorBrandPrimary;

    a {
      margin-left: auto;
      margin-right: 12px;
      background-color: @colorBrandPrimary;
      color: @colorWhite;
      height: 22px;
      padding: 11px 24px 13px 24px;
      font-size: 16px;
      font-weight: bold;
      letter-spacing: 0;
      line-height: 20px;
      text-align: center;
      text-decoration: none;
    }
  }
}
</style>
