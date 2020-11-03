<template>
  <div id="categorization" class="GeneralOverview">
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Categorization') | translate"
      show-legend
    >
      <el-row :gutter="20" type="flex">
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('unicef_sector')"
            :draft-rule="draftRules.unicef_sector"
            :publish-rule="publishRules.unicef_sector"
          >
            <template slot="label">
              <translate key="sector-label">
                Please select the sector(s) the initiative serves.
              </translate>
            </template>

            <multi-selector
              v-model="unicef_sector"
              v-validate="rules.unicef_sector"
              data-vv-name="unicef_sector"
              data-vv-as="UNICEF Sector"
              source="getSectors"
            />
            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>
                  Please select the sector(s) the initiative serves.
                </translate>
              </p>
            </span>
          </custom-required-form-item>
        </el-col>
      </el-row>

      <custom-required-form-item
        :error="errors.first('goal_area')"
        :draft-rule="draftRules.goal_area"
        :publish-rule="publishRules.goal_area"
      >
        <template slot="label">
          <translate key="unicef-goal"> Goal Area </translate>
        </template>

        <GoalAreasSelector
          v-model="goal_area"
          v-validate="rules.goal_area"
          data-vv-name="goal_area"
          data-vv-validate-on="change"
          data-vv-as="Goal Area"
        />
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('result_area')"
        :draft-rule="draftRules.result_area"
        :publish-rule="publishRules.result_area"
      >
        <template slot="label">
          <translate key="result-area"> Result Area </translate>
        </template>

        <ResultAreasSelector
          v-model="result_area"
          v-validate="rules.result_area"
          :goal-area="goal_area"
          data-vv-name="result_area"
          data-vv-validate-on="change"
          data-vv-as="Result Area"
        />
      </custom-required-form-item>

      <template v-if="shoDHAFields">
        <custom-required-form-item
          :error="errors.first('health_focus_areas')"
          :draft-rule="draftRules.health_focus_areas"
          :publish-rule="publishRules.health_focus_areas"
        >
          <template slot="label">
            <translate key="health-focus-areas">
              What is the health focus area(s) addressed by the DHI?
            </translate>
          </template>

          <health-focus-areas-selector
            v-model="health_focus_areas"
            v-validate="rules.health_focus_areas"
            data-vv-name="health_focus_areas"
            data-vv-validate-on="change"
            data-vv-as="Health focus areas"
          />
        </custom-required-form-item>

        <custom-required-form-item
          :error="errors.first('hsc_challenges')"
          :draft-rule="draftRules.hsc_challenges"
          :publish-rule="publishRules.hsc_challenges"
        >
          <template slot="label">
            <translate key="hsc-challenges">
              What are the Health System Challenges addressed by the Digital
              Health Intervention?
            </translate>
          </template>
          <health-system-challenges-selector
            v-model="hsc_challenges"
            v-validate="rules.hsc_challenges"
            data-vv-name="hsc_challenges"
            data-vv-validate-on="change"
            data-vv-as="Health system challenges"
          />
        </custom-required-form-item>
      </template>

      <template v-else-if="goal_area">
        <custom-required-form-item
          v-if="selectedGoalArea.capability_level_question !== 'MISSING'"
          :error="errors.first('capability_levels')"
          :draft-rule="draftRules.capability_levels"
          :publish-rule="publishRules.capability_levels"
        >
          <template slot="label">
            {{ selectedGoalArea.capability_level_question }}
          </template>
          <CapabilitySelector
            v-model="capability_levels"
            :goal-area="goal_area"
            :values-function="getCapabilityLevelsItems"
            data-vv-name="capability_levels"
            data-vv-validate-on="change"
            :data-vv-as="selectedGoalArea.capability_level_question"
          />
        </custom-required-form-item>
        <custom-required-form-item
          v-if="selectedGoalArea.capability_category_question !== 'MISSING'"
        >
          <template slot="label">
            {{ selectedGoalArea.capability_category_question }}
          </template>
          <CapabilitySelector
            v-model="capability_categories"
            :goal-area="goal_area"
            :values-function="getCapabilityCategoriesItems"
          />
        </custom-required-form-item>
        <custom-required-form-item
          v-if="selectedGoalArea.capability_subcategory_question !== 'MISSING'"
        >
          <template slot="label">
            {{ selectedGoalArea.capability_subcategory_question }}
          </template>
          <CapabilitySelector
            v-model="capability_subcategories"
            :goal-area="goal_area"
            :values-function="getCapabilitySubcategoriesItems"
          />
        </custom-required-form-item>
      </template>

      <el-row :gutter="20" type="flex">
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('regional_priorities')"
            :draft-rule="draftRules.regional_priorities"
            :publish-rule="publishRules.regional_priorities"
          >
            <template slot="label">
              <translate key="priorities-label">
                What regional priorities are addressed by the initiative?
              </translate>
            </template>

            <multi-selector
              v-model="regional_priorities"
              v-validate="rules.regional_priorities"
              data-vv-name="regional_priorities"
              data-vv-as="Regional Priorities"
              source="getRegionalPriorities"
            />
            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>
                  Please select the regional priorities addressed by the
                  initiative.
                </translate>
              </p>
            </span>
          </custom-required-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20" type="flex">
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('innovation_categories')"
            :draft-rule="draftRules.innovation_categories"
            :publish-rule="publishRules.innovation_categories"
          >
            <template slot="label">
              <translate key="priorities-label">
                Please select all UNICEF Innovation categories this initiative
                applies to.
              </translate>
            </template>

            <multi-selector
              v-model="innovation_categories"
              v-validate="rules.innovation_categories"
              data-vv-name="innovation_categories"
              data-vv-as="Innovation Categories"
              source="getInnovationCategories"
            />
          </custom-required-form-item>
        </el-col>
      </el-row>
    </collapsible-card>
  </div>
</template>

<script>
import MultiSelector from '@/components/project/MultiSelector'
import { mapGetters } from 'vuex'
import HealthSystemChallengesSelector from '@/components/project/HealthSystemChallengesSelector'
import HealthFocusAreasSelector from '@/components/project/HealthFocusAreasSelector'
import GoalAreasSelector from '@/components/common/GoalAreasSelector'
import ResultAreasSelector from '@/components/common/ResultAreasSelector'
import CapabilitySelector from '@/components/project/CapabilitySelector'
import { mapGettersActions } from '@/utilities/form'
import CollapsibleCard from '../CollapsibleCard'
import ProjectFieldsetMixin from '../../mixins/ProjectFieldsetMixin.js'
import VeeValidationMixin from '../../mixins/VeeValidationMixin.js'

export default {
  components: {
    CollapsibleCard,
    MultiSelector,
    HealthSystemChallengesSelector,
    HealthFocusAreasSelector,
    GoalAreasSelector,
    ResultAreasSelector,
    CapabilitySelector,
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  computed: {
    ...mapGetters({
      modified: 'project/getModified',
      selectedGoalArea: 'project/getGoalAreaDetails',
      getCapabilityLevelsItems: 'projects/getCapabilityLevels',
      getCapabilityCategoriesItems: 'projects/getCapabilityCategories',
      getCapabilitySubcategoriesItems: 'projects/getCapabilitySubcategories',
    }),
    ...mapGettersActions({
      goal_area: ['project', 'getGoalArea', 'setGoalArea', 0],
      result_area: ['project', 'getResultArea', 'setResultArea', 0],
      capability_levels: [
        'project',
        'getCapabilityLevels',
        'setCapabilityLevels',
        0,
      ],
      capability_categories: [
        'project',
        'getCapabilityCategories',
        'setCapabilityCategories',
        0,
      ],
      capability_subcategories: [
        'project',
        'getCapabilitySubcategories',
        'setCapabilitySubcategories',
        0,
      ],
      health_focus_areas: [
        'project',
        'getHealthFocusAreas',
        'setHealthFocusAreas',
        0,
      ],
      hsc_challenges: ['project', 'getHscChallenges', 'setHscChallenges', 0],
      unicef_sector: ['project', 'getSectors', 'setSectors', 0],
      regional_priorities: [
        'project',
        'getRegionalPriorities',
        'setRegionalPriorities',
        0,
      ],
      innovation_categories: [
        'project',
        'getInnovationCategories',
        'setInnovationCategories',
        0,
      ],
    }),
    shoDHAFields() {
      return this.goal_area === 1
    },
  },
  methods: {
    async validate() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([this.$validator.validate()])
      return validations.reduce((a, c) => a && c, true)
    },
    async validateDraft() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([
        this.$validator.validate('unicef_sector'),
        this.$validator.validate('regional_priorities'),
        this.$validator.validate('innovation_categories'),
      ])
      return validations.reduce((a, c) => a && c, true)
    },
  },
}
</script>

<style lang="less"></style>
