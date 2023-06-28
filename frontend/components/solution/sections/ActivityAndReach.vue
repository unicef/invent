<template>
  <div id="activity-and-reach" class="GeneralSolution">
    <collapsible-solution-card
      ref="collapsible"
      key="activity-reach"
      :title="$gettext('Activity and Reach') | translate"
    >
      <el-row>
        <simple-field
          :header="$gettext('Global reach of this solution') | translate"
          :content="innerValue.people_reached"
        />
      </el-row>

      <el-row :gutter="20" type="flex">
        <el-col :span="6">
          <custom-required-form-item :error="errors.first('override_reach')" :publish-rule="rules.override_reach">
            <template slot="label">
              <translate key="override_reach">Override reach value</translate>
            </template>

            <el-input-number
              v-model.number="innerValue.override_reach"
              v-validate="rules.override_reach"
              data-vv-name="override_reach"
              data-vv-as="Override reach value"
              :controls="false"
              controls-position="left"
              class="number-input"
              placeholder=" "
              :min="0"
              data-test="override-reach-input"
            />
          </custom-required-form-item>
        </el-col>
        <el-col :span="12"> </el-col>
      </el-row>
      <el-row>
        <countries-table-input v-model="innerValue.country_solutions" :rules="rules" />
      </el-row>
    </collapsible-solution-card>
  </div>
</template>

<script>
import VeeValidationMixin from '@/components/mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '@/components/mixins/ProjectFieldsetMixin.js'
import CollapsibleSolutionCard from '../CollapsibleSolutionCard.vue'
import SimpleField from '@/components/project/SimpleField'
import CountriesTableInput from '../CountriesTableInput.vue'

export default {
  components: {
    CollapsibleSolutionCard,
    SimpleField,
    CountriesTableInput,
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
    value: Object,
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
      console.log('General overview published validation', validations)
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

.TeamArea {
  position: relative;
}
.number-input {
  width: 90%;
  &.el-input-number .el-input__inner {
    text-align: left;
  }
}
</style>
