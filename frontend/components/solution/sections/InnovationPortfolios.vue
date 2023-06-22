<template>
  <div id="innovationPortfolios" class="InnovationSolution">
    <collapsible-solution-card
      ref="collapsible"
      key="innovationPortfolios"
      :title="$gettext('Innovation Portfolios') | translate"
      show-legend
    >
      <portfolio-table-input
        v-model="innerValue.portfolio_problem_statements"
        v-validate="rules.portfolio_statements_table"
        :rules="rules"
        :error="errors.first('portfolio-table')"
        name="portfolio-table"
        class="portfolio-table"
      />

      <custom-required-form-item
        :error="errors.first('phase') ? errors.first('phase').replace('_', ' ') : undefined"
        :publish-rule="rules.phase"
      >
        <template slot="label">
          <translate key="phase"> Phase </translate>
        </template>

        <SolutionPhaseSelect v-model="innerValue.phase" data-test="solution-phase-select" />
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('tech') ? errors.first('tech').replace('_', ' ') : undefined"
        :draft-rule="rules.tech"
        :publish-rule="rules.tech"
      >
        <el-checkbox
          v-model="innerValue.open_source_frontier_tech"
          class="tech__checkbox"
          :label="'tech'"
          data-test="solution-tech-checkbox"
          ><translate>Open source frontier tech</translate>
        </el-checkbox>
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('learning') ? errors.first('learning').replace('_', ' ') : undefined"
        :draft-rule="rules.learning"
        :publish-rule="rules.learning"
      >
        <el-checkbox
          v-model="innerValue.learning_investment"
          class="tech__checkbox"
          :label="'investment'"
          data-test="solution-learning-checkbox"
          ><translate>Learning investment</translate>
        </el-checkbox>
      </custom-required-form-item>
    </collapsible-solution-card>
  </div>
</template>

<script>
import VeeValidationMixin from '@/components/mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '@/components/mixins/ProjectFieldsetMixin.js'
import CollapsibleSolutionCard from '../CollapsibleSolutionCard.vue'
import SolutionPhaseSelect from '../SolutionPhaseSelect.vue'
import PortfolioTableInput from '../PortfolioTableInput.vue'

export default {
  components: {
    CollapsibleSolutionCard,
    SolutionPhaseSelect,
    PortfolioTableInput,
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    publishRules: {
      required: false,
    },
    draftRules: {
      required: false,
    },
    value: {
      required: false,
    },
  },

  computed: {
    innerValue: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('change', value)
      },
    },
  },

  methods: {
    async validate() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([this.$validator.validate()])
      return validations.reduce((a, c) => a && c, true)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.InnovationSolution {
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
  .el-checkbox__label {
    font-weight: bold;
  }

  .el-checkbox__inner {
    border-color: @colorTextPrimary;
  }
}
.TeamArea {
  position: relative;
}
.portfolio-table {
  padding-top: 16px;
  padding-bottom: 18px;
}
</style>
