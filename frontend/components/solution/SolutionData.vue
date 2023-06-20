<template>
  <div class="SolutionData" v-if="solution">
    <el-row type="flex">
      <!-- <el-col :span="18"> -->
      <el-col>
        <collapsible-card id="general" :title="$gettext('1. General') | translate">
          <simple-field :content="solution.name" :header="$gettext('Name') | translate" />
        </collapsible-card>

        <collapsible-card id="innovation-portfolios" :title="$gettext('2. Innovation portfolios') | translate">
          <simple-field :header="$gettext('Innovation portfolios and problem statements') | translate">
            <PortfolioTable :portfoliosProblemStatements="solution.portfolio_problem_statements" />
          </simple-field>

          <simple-field :header="$gettext('Phase') | translate" :content="phaseName" />

          <simple-field
            :content="yesNo(solution.open_source_frontier_tech)"
            :header="$gettext('Open source frontier tech') | translate"
          />

          <simple-field
            :content="yesNo(solution.learning_investment)"
            :header="$gettext('Learning investment') | translate"
          />
        </collapsible-card>

        <collapsible-card id="activity-and-reach" :title="$gettext('3. Activity and Reach') | translate">
          <simple-field :header="$gettext('Global reach of this solution') | translate" :content="peopleReached" />

          <simple-field :header="$gettext('Countries where this solution is active') | translate">
            <CountriesTable :tableData="solution.country_solutions" />
          </simple-field>
        </collapsible-card>
      </el-col>
      <!-- <el-col :span="6">
        <SolutionNavigation
          @handleClickUnPublish="
            handleClickUnPublish(
              {
                name: 'organisation-initiatives-id-edit',
                params: { ...$route.params },
              },
              $route.params.id
            )
          "
          @handleClickLatest="handleClickLatest($route.params.id)"
        />
      </el-col> -->
    </el-row>
  </div>
</template>

<script>
// vuex
import { mapGetters } from 'vuex'

// components
import SolutionNavigation from './SolutionNavigation'
import CollapsibleCard from '@/components/project/CollapsibleCard'
import SimpleField from '@/components/project/SimpleField'
import PortfolioTable from './PortfolioTable.vue'
import CountriesTable from './CountriesTable.vue'

export default {
  components: {
    SolutionNavigation,
    CollapsibleCard,
    SimpleField,
    PortfolioTable,
    CountriesTable,
  },
  computed: {
    ...mapGetters({
      solution: 'solution/getSolutionData',
      phases: 'system/getSolutionPhases',
    }),

    route() {
      return this.$route.name.split('__')[0]
    },
    isDraft() {
      //return this.route === 'organisation-porfolio-innovation-solutions-id-edit'
    },
    project() {
      return this.isDraft ? this.draft : this.published
    },
    peopleReached() {
      return this.solution.people_reached === 0 ? '0' : this.solution.people_reached
    },
    phaseName() {
      return this.phases.find((phase) => phase.id === this.solution.phase).name
    },
  },
  methods: {
    yesNo(booleanParam) {
      return booleanParam ? this.$gettext('Yes') : this.$gettext('No')
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.SolutionData {
  .limitPageWidth();

  .cover {
    max-width: 100%;
  }

  .Loader {
    display: block;
    margin: 0 auto 80px;
  }

  > .el-row {
    > .el-col {
      width: 90%;
      margin: auto;
    }
  }

  .ContentContainer {
    padding-bottom: 20px;
  }

  .CollapsibleCard {
    .SimpleField {
      margin-bottom: 40px;
      font-size: @fontSizeBase;
      line-height: 20px;

      .Header {
        margin-bottom: 10px;
        font-size: @fontSizeMedium;
        font-weight: 700;
      }

      .Content {
        ul {
          li {
            .svg-inline--fa {
              display: none;
            }
          }
        }
      }

      .SubLevelItem {
        box-sizing: border-box;
        width: 100%;
        margin-top: 10px;
        margin-bottom: 10px;
        margin-left: 3px;
        padding-left: 30px;
        border-left: 5px solid @colorGrayLight;

        .SimpleField {
          margin: 0 !important;

          .Header {
            font-size: @fontSizeBase !important;
          }
        }
      }
    }

    .GrayArea {
      .svg-inline--fa {
        margin-right: 8px;
      }
    }
  }
  .ma-0 {
    margin: 0;
  }
}
</style>
