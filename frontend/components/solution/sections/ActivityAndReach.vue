<template>
  <div id="activity-and-reach" class="GeneralSolution">
    <collapsible-solution-card ref="collapsible" key="general" :title="$gettext('Activity and Reach') | translate">
      <el-row>
        <simple-field
          :header="$gettext('Global reach of this solution') | translate"
          :content="getSolutionData.people_reached"
        />
      </el-row>

      <el-row :gutter="20" type="flex">
        <el-col :span="6">
          <custom-required-form-item :error="errors.first('override_reach')" :publish-rule="rules.override_reach">
            <template slot="label">
              <translate key="override_reach">Override reach value</translate>
            </template>

            <character-count-input
              v-model="override_reach"
              v-validate="rules.override_reach"
              :rules="rules.override_reach"
              data-vv-name="override_reach"
              data-vv-as="Override reach value"
            />
          </custom-required-form-item>
        </el-col>
        <el-col :span="12"> </el-col>
      </el-row>
      <el-row>
        <countries-table-input
          :tableData="getSolutionData.country_solutions"
          @update-countries="updateCountriesTable"
        />
      </el-row>
    </collapsible-solution-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import CustomRequiredFormTeamItem from '@/components/proxy/CustomRequiredFormTeamItem'
import VeeValidationMixin from '@/components/mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '@/components/mixins/ProjectFieldsetMixin.js'
import CollapsibleSolutionCard from '../CollapsibleSolutionCard.vue'
import SimpleField from '@/components/project/SimpleField'
import CountriesTableInput from '../CountriesTableInput.vue'

export default {
  components: {
    CollapsibleSolutionCard,
    CustomRequiredFormTeamItem,
    SimpleField,
    CountriesTableInput,
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  props: {
    publishRules: {
      required: false,
    },
    draftRules: {
      required: false,
    },
  },
  data: function () {
    return {
      override_reach: 0,
    }
  },
  computed: {
    ...mapGetters({
      getSolutionData: 'solution/getSolutionData',
    }),
  },
  watch: {
    async country_office() {
      if (this.officeData) {
        await this.$store.dispatch('countries/loadCountryDetails', this.officeData.country)
        this.country = this.officeData.country
      }
    },
  },
  methods: {
    updateCountriesTable(countriesArray) {
      // assign new countries value
    },
    async validate() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([this.$validator.validate()])
      console.log('General overview published validation', validations)
      return validations.reduce((a, c) => a && c, true)
    },
    async validateDraft() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([
        this.$validator.validate('name'),
        this.$validator.validate('country_office'),
      ])
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
</style>
