<template>
  <div id="general" class="GeneralSolution">
    <collapsible-solution-card ref="collapsible" key="general" :title="$gettext('General') | translate" show-legend>
      <custom-required-form-item :error="errors.first('name')" :publish-rule="rules.name">
        <template slot="label">
          <translate key="solution-name"> What is the name of the solution? </translate>
        </template>
        <template slot="tooltip">
          <el-tooltip
            class="item"
            content="Suggested format for the initiative name: Prefix (RO or CO) -
              (Sector or Function) - Name of Initiative (Identifier). Example: PHL - T4D -
              Knowledge, Innovation and Data System (KIDS)"
            placement="right"
          >
            <i class="el-icon-warning warning" />
          </el-tooltip>
        </template>

        <character-count-input
          v-model="solution.name"
          v-validate="rules.name"
          :rules="rules.name"
          data-as-name="Name"
          data-vv-name="name"
        />
        <span class="Hint">
          <fa icon="info-circle" />
          <p>
            <translate>
              A short and memorable name for this solution. This name will be used across all implementing countries,
              and will allow colleagues to find and remember the solution. This should match any public-facing name for
              this solution.
            </translate>
          </p>
        </span>
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('phase') ? errors.first('phase').replace('_', ' ') : undefined"
        :publish-rule="rules.phase"
      >
        <template slot="label">
          <translate key="phase"> Phase </translate>
        </template>

        <SolutionPhaseSelect v-model="solution.phase" />
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('tech') ? errors.first('tech').replace('_', ' ') : undefined"
        :draft-rule="rules.tech"
        :publish-rule="rules.tech"
      >
        <el-checkbox :v-model="solution.open_source_frontier_tech" class="tech__checkbox" :label="'tech'"
          ><translate>Open source frontier tech</translate>
        </el-checkbox>
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('learning') ? errors.first('learning').replace('_', ' ') : undefined"
        :draft-rule="rules.learning"
        :publish-rule="rules.learning"
      >
        <el-checkbox :v-model="solution.learning_investment" class="tech__checkbox" :label="'investment'"
          ><translate>Learning investment</translate>
        </el-checkbox>
      </custom-required-form-item>
      <portfolio-table-input :tableData="solution.portfolio_problem_statements" @change="" />
    </collapsible-solution-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import CustomRequiredFormTeamItem from '@/components/proxy/CustomRequiredFormTeamItem'
import VeeValidationMixin from '@/components/mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '@/components/mixins/ProjectFieldsetMixin.js'
import CollapsibleSolutionCard from '../CollapsibleSolutionCard.vue'
import TeamSelector from '@/components/project/TeamSelector'
import SolutionPhaseSelect from '../SolutionPhaseSelect.vue'
import PortfolioTableInput from '../PortfolioTableInput.vue'

export default {
  components: {
    CollapsibleSolutionCard,
    SolutionPhaseSelect,
    TeamSelector,
    CustomRequiredFormTeamItem,
    PortfolioTableInput,
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  data: function () {
    return {
      solution: {
        name: '',
        phase: 0,
        open_source_frontier_tech: false,
        learning_investment: false,
        portfolio_problem_statements: [],
        country_solutions: [],
        people_reached: 0,
      },
    }
  },
  computed: {
    ...mapGetters({
      unicef_regions: 'system/getUnicefRegions',
      getCountryDetails: 'countries/getCountryDetails',
      modified: 'project/getModified',
      regionalOffices: 'projects/getRegionalOffices',
      userProfiles: 'system/getUserProfilesNoFilter',
      getStatements: 'portfolio/getStatements',
      getPortfolios: 'portfolio/getPortfolios',
      getSolution: 'solution/getSolutionData',
    }),
  },
  mounted: function () {
    const s = this.getSolution
    this.solution = {
      ...this.solution,
      name: s.name,
      phase: s.phase,
      open_source_frontier_tech: s.open_source_frontier_tech,
      learning_investment: s.learning_investment,
      country_solutions: s.country_solutions,
      portfolio_problem_statements: s.portfolio_problem_statements,
      people_reached: s.people_reached,
    }
  },
  watch: {
    getSolution: function () {
      const s = this.getSolution
      this.solution = {
        ...this.solution,
        name: s.name,
        phase: s.phase,
        open_source_frontier_tech: s.open_source_frontier_tech,
        learning_investment: s.learning_investment,
        country_solutions: s.country_solutions,
        portfolio_problem_statements: s.portfolio_problem_statements,
        people_reached: s.people_reached,
      }
    },
  },
  methods: {
    async validate() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([this.$validator.validate()])
      console.log('General overview published validation', validations)
      return validations.reduce((a, c) => a && c, true)
    },
    async validateDraft() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([this.$validator.validate('name'), this.$validator.validate('phase')])
      console.log('General overview draft validation', validations)
      return validations.reduce((a, c) => a && c, true)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.GeneralSolution {
  .CountrySelector,
  .select-office {
    width: 100%;
  }

  .Date {
    width: 100% !important;
  }

  .no-padding {
    padding-top: 0;
    padding-bottom: 0;
  }
  .ma-0 {
    margin: 0;
  }
}
.tech__checkbox {
  color: @colorTextPrimary;
  .el-checkbox__inner {
    border-color: @colorTextPrimary;
  }
}
.TeamArea {
  position: relative;
}
</style>
