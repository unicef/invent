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
          v-model="innerValue.name"
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

        <SolutionPhaseSelect v-model="innerValue.phase" />
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('tech') ? errors.first('tech').replace('_', ' ') : undefined"
        :draft-rule="rules.tech"
        :publish-rule="rules.tech"
      >
        <el-checkbox v-model="innerValue.open_source_frontier_tech" class="tech__checkbox" :label="'tech'"
          ><translate>Open source frontier tech</translate>
        </el-checkbox>
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('learning') ? errors.first('learning').replace('_', ' ') : undefined"
        :draft-rule="rules.learning"
        :publish-rule="rules.learning"
      >
        <el-checkbox v-model="innerValue.learning_investment" class="tech__checkbox" :label="'investment'"
          ><translate>Learning investment</translate>
        </el-checkbox>
      </custom-required-form-item>
      <portfolio-table-input
        v-model="innerValue.portfolio_problem_statements"
        v-validate="rules.portfolio_statements_table"
        :rules="rules"
        :error="errors.first('portfolio-table')"
        name="portfolio-table"
      />
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
</style>
