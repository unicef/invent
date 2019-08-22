<template>
  <div
    id="implementation"
    class="ImplementationOverview"
  >
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Implementation overview') | translate"
      show-legend
    >
      <custom-required-form-item
        :error="errors.first('goal_area')"
        :draft-rule="draftRules.goal_area"
        :publish-rule="publishRules.goal_area"
      >
        <template slot="label">
          <translate key="unicef-goal">
            Goal Area
          </translate>
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
          <translate key="result-area">
            Result Area
          </translate>
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
              What are the Health System Challenges addressed by the Digital Health Intervention?
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

        <custom-required-form-item
          :error="errors.first('strategies')"
          :draft-rule="draftRules.strategies"
          :publish-rule="publishRules.strategies"
          class="DigitalHealthIntervention"
        >
          <template slot="label">
            <translate key="strategies">
              What is the health capability area(s) addressed? What are the Health System Challenges addressed by the Digital Health Intervention?
            </translate>
            <form-hint>
              Form Hint
            </form-hint>
          </template>
          <digital-health-interventions-selector
            v-validate="rules.strategies"
            data-vv-name="strategies"
            data-vv-as="Digital health interventions"
          />
        </custom-required-form-item>
      </template>

      <template v-else-if="goal_area">
        <custom-required-form-item
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
        <custom-required-form-item>
          <template slot="label">
            {{ selectedGoalArea.capability_category_question }}
          </template>
          <CapabilitySelector
            v-model="capability_categories"
            :goal-area="goal_area"
            :values-function="getCapabilityCategoriesItems"
          />
        </custom-required-form-item>
        <custom-required-form-item>
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

      <custom-required-form-item
        :error="errors.first('platforms')"
        :draft-rule="draftRules.platforms"
        :publish-rule="publishRules.platforms"
      >
        <template slot="label">
          <translate key="platform-label">
            What are the names of the software included in the deployment?
          </translate>
        </template>

        <platform-selector
          v-model="platforms"
          v-validate="rules.platforms"
          data-vv-name="platforms"
          data-vv-as="Software"
        />
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('donors')"
        :draft-rule="draftRules.donors"
        :publish-rule="publishRules.donors"
      >
        <template slot="label">
          <translate key="donors">
            Who are your investment partners?
          </translate>
          <form-hint>
            <translate key="donors-hint">
              Investment partners can include those contributing funds, human resources or in-kind support.
            </translate>
          </form-hint>
        </template>

        <donor-selector
          v-model="donors"
          v-validate="rules.donors"
          data-vv-name="donors"
          data-vv-as="Investors"
        />
      </custom-required-form-item>
    </collapsible-card>
  </div>
</template>

<script>
import VeeValidationMixin from '../../mixins/VeeValidationMixin.js';
import ProjectFieldsetMixin from '../../mixins/ProjectFieldsetMixin.js';

import CollapsibleCard from '../CollapsibleCard';
import HealthSystemChallengesSelector from '../HealthSystemChallengesSelector';
import HealthFocusAreasSelector from '../HealthFocusAreasSelector';
import GoalAreasSelector from '@/components/common/GoalAreasSelector';
import ResultAreasSelector from '@/components/common/ResultAreasSelector';
import CapabilitySelector from '../CapabilitySelector';
import PlatformSelector from '../PlatformSelector';
import DigitalHealthInterventionsSelector from '../DigitalHealthInterventionsSelector';
import DonorSelector from '../DonorSelector';
import FormHint from '../FormHint';

import { mapGettersActions } from '../../../utilities/form';
import { mapGetters } from 'vuex';

export default {
  components: {
    CollapsibleCard,
    HealthSystemChallengesSelector,
    HealthFocusAreasSelector,
    GoalAreasSelector,
    ResultAreasSelector,
    CapabilitySelector,
    PlatformSelector,
    DigitalHealthInterventionsSelector,
    DonorSelector,
    FormHint
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],

  computed: {
    ...mapGetters({
      selectedGoalArea: 'project/getGoalAreaDetails',
      getCapabilityLevelsItems: 'projects/getCapabilityLevels',
      getCapabilityCategoriesItems: 'projects/getCapabilityCategories',
      getCapabilitySubcategoriesItems: 'projects/getCapabilitySubcategories'
    }),
    ...mapGettersActions({
      goal_area: ['project', 'getGoalArea', 'setGoalArea', 0],
      result_area: ['project', 'getResultArea', 'setResultArea', 0],
      capability_levels: ['project', 'getCapabilityLevels', 'setCapabilityLevels', 0],
      capability_categories: ['project', 'getCapabilityCategories', 'setCapabilityCategories', 0],
      capability_subcategories: ['project', 'getCapabilitySubcategories', 'setCapabilitySubcategories', 0],
      platforms: ['project', 'getPlatforms', 'setPlatforms', 0],
      digitalHealthInterventions: ['project', 'getDigitalHealthInterventions', 'setDigitalHealthInterventions', 0],
      health_focus_areas: ['project', 'getHealthFocusAreas', 'setHealthFocusAreas', 0],
      hsc_challenges: ['project', 'getHscChallenges', 'setHscChallenges', 0],
      donors: ['project', 'getDonors', 'setDonors', 0]
    }),
    shoDHAFields () {
      return this.goal_area === 1;
    }
  },
  methods: {
    async validate () {
      this.$refs.collapsible.expandCard();
      const validations = await Promise.all([
        this.$validator.validate()
      ]);
      console.log('Implementation overview validations', validations);
      return validations.reduce((a, c) => a && c, true);
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .ImplementationOverview {
    .DigitalHealthIntervention {
      margin-top: 30px;
    }

    .CoverageArea {
      .CoverageSubtitle {
        position: relative;
        display: block;
        margin: 0 0 20px;
        padding: 10px 0 0 20px;
        font-size: @fontSizeSmall;
        font-weight: 700;
        color: @colorGray;
        text-transform: uppercase;

        .svg-inline--fa {
          position: absolute;
          top: 10px;
          left: 0;
        }
      }
    }
  }
</style>
