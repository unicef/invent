<template>
  <section class="portfolio-area">
    <div class="content-area">
      <div class="portfolio">
        <!-- tabs -->
        <tabs :tabs="tabs" :tab="tab" :center="false" @handleTab="setTab">
          <template slot="title">
            <div class="PHeader">
              <h2>
                <translate>Portfolio</translate>:
                <el-dropdown
                  trigger="click"
                  placement="bottom-start"
                  @command="navigate"
                >
                  <span class="Title el-dropdown-link">
                    {{ name }} <i class="el-icon-caret-bottom el-icon--right" />
                  </span>
                  <el-dropdown-menu slot="dropdown" class="PDropdown">
                    <el-dropdown-item
                      v-for="portfolio in portfolios"
                      :key="portfolio.id"
                      :command="portfolio.id"
                    >
                      {{ portfolio.name }}
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </h2>
            </div>
          </template>
        </tabs>
        <section class="tab-content">
          <Matrix
            v-show="tab === 1"
            ref="ambitionMatrix"
            bg-image="/bg-ambition_matrix.svg"
            :description="description"
            :elements="ambitionMatrix"
            :left="matrixLabels.ambition.left"
            :bottom="matrixLabels.ambition.bottom"
          />
          <div v-if="tab === 1" class="Problems problem-matrix">
            <el-row>
              <div class="Info">
                <fa icon="info-circle" />
                <translate>
                  The innovation ambition matrix is a strategic framework that
                  helps balance risk and impact. “Newer” challenges and
                  solutions are not necessarily advantageous; rather, the goal
                  is to appropriately balance resource allocation across the
                  incremental, substantial, and breakthrough categories.
                </translate>
              </div>
            </el-row>
          </div>
          <Matrix
            v-show="tab === 2"
            ref="riskMatrix"
            bg-color="#FCEFE8"
            color="#F26A21"
            noarrow
            :description="description"
            :elements="riskImpactMatrix"
            :left="matrixLabels.riskImpact.left"
            :bottom="matrixLabels.riskImpact.bottom"
            :extra-bottom="impactInfo"
            :extra-left="riskInfo"
          />
          <div v-if="tab === 3" class="Problems">
            <el-row type="flex">
              <el-col
                v-for="(col, index) in matrixLabels.problemStatement"
                :key="col"
                :span="8"
              >
                <div :class="`Problem Problem${index + 1}`">
                  <div class="Title">
                    {{ col }}
                  </div>
                  <div>
                    <radio
                      v-for="statement in problemStatementMatrix[index]"
                      :key="statement.id"
                      :value="ps === statement.id"
                      :disabled="disabledProblems.indexOf(statement.id) !== -1"
                      @update="select(statement.id, $event)"
                    >
                      {{ statement.title }}
                    </radio>
                  </div>
                </div>
              </el-col>
            </el-row>
            <el-row>
              <div class="Info">
                <fa icon="info-circle" />
                <translate>
                  By clicking on a problem statement you can add or remove it
                  from your current filter settings.
                </translate>
              </div>
            </el-row>
          </div>
          <search-map v-if="tab === 4" />
        </section>
        <!-- tabs -->
        <div class="DashboardListView">
          <el-row>
            <table-top-actions />
          </el-row>
          <el-row>
            <main-table />
          </el-row>
        </div>
      </div>
    </div>
    <aside class="filter-area">
      <advanced-search />
    </aside>
  </section>
</template>

<script>
import MainTable from '@/components/portfolio/dashboard/MainTable'
import TableTopActions from '@/components/portfolio/dashboard/TableTopActions'
import AdvancedSearch from '@/components/search/AdvancedSearch'
import Matrix from '@/components/portfolio/Matrix'
import Radio from '@/components/portfolio/form/inputs/Radio'
import SearchMap from '@/components/searchMap/SearchMap'
import Tabs from '@/components/common/Tabs'

import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  components: {
    Matrix,
    Radio,
    MainTable,
    AdvancedSearch,
    TableTopActions,
    SearchMap,
    Tabs,
  },
  data() {
    return {
      activeName: 'ambition',
      disabledProblems: [],
      riskInfo: this.$gettext(
        'What are the risk levels associated with this initiative? Note that low scores indicate high risk assessment.'
      ),
      impactInfo: this.$gettext(
        'Impact score takes into account an initiative’s reach, effectiveness, and ability to address key challenges, particularly for vulnerable and hard-to-reach children.'
      ),

      matrixLabels: {
        problemStatement: [
          this.$gettext('Neglected'),
          this.$gettext('Moderate'),
          this.$gettext('High activity'),
        ],
        riskImpact: {
          left: [
            this.$gettext('high'),
            this.$gettext('risk'),
            this.$gettext('low'),
          ],
          bottom: [
            this.$gettext('low'),
            this.$gettext('impact (total global need)'),
            this.$gettext('high'),
          ],
        },
        ambition: {
          left: [
            this.$gettext('existing'),
            this.$gettext('challenge'),
            this.$gettext('new'),
          ],
          bottom: [
            this.$gettext('existing'),
            this.$gettext('solution (tools)'),
            this.$gettext('new'),
          ],
        },
      },
      // tabs information handle
      tabs: [
        {
          id: 1,
          name: this.$gettext('ambition matrix'),
          icon: 'braille',
        },
        {
          id: 2,
          name: this.$gettext('risk-impact matrix'),
          icon: 'th',
        },
        {
          id: 3,
          name: this.$gettext('problem statement matrix'),
          icon: 'columns',
        },
        {
          id: 4,
          name: this.$gettext('map view'),
          icon: 'globe-africa',
        },
      ],
      tab: 1,
    }
  },
  async fetch({ store, query, error, params }) {
    // setup search
    store.dispatch('search/resetSearch')
    await store.dispatch('dashboard/setSearchOptions', query)
    store.commit('search/SET_SEARCH', { key: 'portfolio', val: params.id })
    store.commit('search/SET_SEARCH', {
      key: 'portfolio_page',
      val: 'portfolio',
    })
    store.commit('search/SET_SEARCH', { key: 'scores', val: true })
    // set portfolio details
    store.commit('portfolio/SET_VALUE', {
      key: 'currentPortfolioId',
      val: params.id,
    })
    // actual search
    await Promise.all([
      store.dispatch('projects/loadProjectStructure'),
      store.dispatch('portfolio/getPortfolioDetails', {
        id: params.id,
        type: 'active-list',
      }),
      store.dispatch('search/getSearch'),
      // map
      store.dispatch('search/loadProjectsMap'),
      store.dispatch('countries/loadMapData'),
    ])
  },

  computed: {
    ...mapState({
      ps: (state) => state.search.filter.ps,
      portfolios: (state) => state.portfolio.portfolios,
    }),
    ...mapGetters({
      ambitionMatrix: 'matrixes/getAmbitionMatrix',
      riskImpactMatrix: 'matrixes/getRiskImpactMatrix',
      problemStatementMatrix: 'matrixes/getProblemStatementMatrix',
      name: 'portfolio/getName',
      description: 'portfolio/getDescription',
    }),
  },
  methods: {
    ...mapActions({
      loadProjectsMap: 'search/loadProjectsMap',
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
      this.$store.dispatch('search/getSearch')
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
