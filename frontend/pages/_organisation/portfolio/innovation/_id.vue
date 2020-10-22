<template>
  <section class="portfolio-area">
    <div class="content-area">
      <div class="portfolio">
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
        <el-tabs v-model="activeName">
          <el-tab-pane
            :label="$gettext('AMBITION MATRIX') | translate"
            name="ambition"
          >
            <Matrix
              ref="ambitionMatrix"
              bg-image="/bg-ambition_matrix.svg"
              :description="description"
              :elements="ambitionMatrix"
              :left="matrixLabels.ambition.left"
              :bottom="matrixLabels.ambition.bottom"
              :contacts="managers"
            />
          </el-tab-pane>
          <el-tab-pane
            :label="$gettext('RISK-IMPACT MATRIX') | translate"
            name="risk"
          >
            <Matrix
              ref="riskMatrix"
              bg-color="#FCEFE8"
              color="#F26A21"
              noarrow
              :description="description"
              :elements="riskImpactMatrix"
              :left="matrixLabels.riskImpact.left"
              :bottom="matrixLabels.riskImpact.bottom"
              :contacts="managers"
              extra-bottom="Quid securi etiam tamquam eu fugiat nulla pariatur. Vivamus sagittis lacus vel augue laoreet rutrum faucibus. Contra legem facit qui id facit quod lex prohibet."
              extra-left="Quid securi etiam tamquam eu fugiat nulla pariatur. Vivamus sagittis lacus vel augue laoreet rutrum faucibus. Contra legem facit qui id facit quod lex prohibet."
            />
          </el-tab-pane>
          <el-tab-pane
            :label="$gettext('PROBLEM STATEMENT MATRIX') | translate"
            name="problem"
          >
            <div class="Problems">
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
                        :disabled="
                          disabledProblems.indexOf(statement.id) !== -1
                        "
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
                  <i class="fas fa-info-circle" />
                  <translate>
                    By clicking on a problem statement you can add or remove it
                    from your current filter settings.
                  </translate>
                </div>
              </el-row>
            </div>
          </el-tab-pane>
          <el-tab-pane :label="$gettext('MAP VIEW') | translate" name="map">
            TODO
          </el-tab-pane>
        </el-tabs>

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
import { mapState, mapGetters } from 'vuex'

export default {
  components: {
    Matrix,
    Radio,
    MainTable,
    AdvancedSearch,
    TableTopActions,
  },
  data() {
    return {
      activeName: 'ambition',
      disabledProblems: [],
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
    }
  },
  async fetch({ store, query, error, params }) {
    // setup search
    store.dispatch('search/resetSearch')
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
      store.dispatch('portfolio/getPortfolios'),
      store.dispatch('projects/loadProjectStructure'),
      store.dispatch('portfolio/getPortfolioDetails', params.id),
      store.dispatch('search/getSearch'),
    ])
  },

  computed: {
    ...mapState({
      ps: (state) => state.search.filter.ps,
    }),
    ...mapGetters({
      ambitionMatrix: 'matrixes/getAmbitionMatrix',
      riskImpactMatrix: 'matrixes/getRiskImpactMatrix',
      problemStatementMatrix: 'matrixes/getProblemStatementMatrix',
      name: 'portfolio/getName',
      managers: 'portfolio/getManagers',
      description: 'portfolio/getDescription',
      portfolios: 'portfolio/getActivePortfolios',
    }),
  },
  methods: {
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
    select(val) {
      this.$store.commit('search/SET_SEARCH', { key: 'ps', val })
      this.$store.dispatch('search/getSearch')
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';
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
  //margin: 0 40px 160px 40px;
  margin-bottom: 80px;
  .PHeader {
    padding: 0 40px;
    background-color: white;
  }
  &::v-deep .el-tabs {
    .el-tabs__header {
      padding: 0 40px;
      background-color: white;
    }
    .el-tabs__nav-wrap::after {
      background-color: transparent;
    }
    .el-tabs__active-bar {
      height: 3px;
      background-color: #1cabe2;
    }
    .el-tabs__content {
      margin: 0 40px;
      padding-top: 40px;
    }
    .el-tabs__item {
      color: #777779;
      &.is-active,
      &:hover {
        color: #404041;
      }
      &:hover {
        font-weight: bold;
      }
    }
  }
  &::v-deep .el-tabs__nav {
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 0;
    line-height: 18px;

    & > div:before {
      font-family: 'Font Awesome 5 Free';
      -moz-osx-font-smoothing: grayscale;
      -webkit-font-smoothing: antialiased;
      display: inline-block;
      font-style: normal;
      font-feature-settings: normal;
      font-variant: normal;
      text-rendering: auto;
      line-height: 1;
      font-weight: 900;
      margin-right: 8px;
    }
    & > div:first-child {
      & + div {
        &:before {
          content: '\f2a1';
        }
      }
      & + div + div {
        &:before {
          content: '\f00a';
        }
      }
      & + div + div + div {
        &:before {
          content: '\f0db';
        }
      }
      & + div + div + div + div {
        &:before {
          content: '\f57c';
        }
      }
    }
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
    padding: 50px 0 24px 0;
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
