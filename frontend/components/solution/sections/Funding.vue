<template>
  <div id="funding" class="InnovationSolution">
    <collapsible-solution-card ref="collapsible" key="funding" :title="$gettext('Funding') | translate" show-legend>
      <custom-required-form-item
        :error="errors.first('setAside2021') ? errors.first('setAside2021').replace('_', ' ') : undefined"
        :draft-rule="rules.setAside2021"
        :publish-rule="rules.setAside2021"
      >
        <el-checkbox
          v-model="innerValue.set_aside_2021"
          class="setaside__checkbox"
          :label="'setAside2021'"
          data-test="solution-setAside2021-checkbox"
          ><translate>Set Aside 2021</translate>
        </el-checkbox>
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('setAside2022') ? errors.first('setAside2022').replace('_', ' ') : undefined"
        :draft-rule="rules.setAside2022"
        :publish-rule="rules.setAside2022"
      >
        <el-checkbox
          v-model="innerValue.set_aside_2022"
          class="setaside__checkbox"
          :label="'setAside2022'"
          data-test="solution-setAside2022-checkbox"
          ><translate>Set Aside 2022</translate>
        </el-checkbox>
      </custom-required-form-item>
    </collapsible-solution-card>
  </div>
</template>

<script>
import VeeValidationMixin from '@/components/mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '@/components/mixins/ProjectFieldsetMixin.js'
import CollapsibleSolutionCard from '../CollapsibleSolutionCard.vue'

export default {
  components: {
    CollapsibleSolutionCard,
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
.setaside__checkbox {
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
