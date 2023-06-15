<template>
  <div id="categorization" class="GeneralOverview">
    <collapsible-card ref="collapsible" :title="$gettext('Categorization') | translate" show-legend>
      <el-row :gutter="20" type="flex">
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('unicef_leading_sector')"
            :draft-rule="draftRules.unicef_leading_sector"
            :publish-rule="publishRules.unicef_leading_sector"
          >
            <template slot="label">
              <translate key="leading-sector-label"> Please select the Lead sector the initiative serves. </translate>
            </template>

            <multi-selector-platform
              v-model="unicef_leading_sector"
              v-validate="rules.unicef_leading_sector"
              data-vv-name="unicef_leading_sector"
              data-vv-as="UNICEF Leading Sector"
              source="getLeadingSector"
              :multiple="false"
            />
            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>
                  UNICEF's programmes emphasize developing community-level services to promote the health and well-being
                  of children via interventions in health, child protection, social policy, education etc. An initiative
                  is cross-sectoral if it falls in more than one sector or programme area e.g. Introduction of latrines
                  in schools falls in both WASH as well as Education.
                </translate>
              </p>
            </span>
          </custom-required-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20" type="flex">
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('unicef_supporting_sectors')"
            :draft-rule="draftRules.unicef_supporting_sectors"
            :publish-rule="publishRules.unicef_supporting_sectors"
          >
            <template slot="label">
              <translate key="sector-label"> Please select the Supporting sector(s) the initiative serves. </translate>
            </template>

            <multi-selector-platform
              v-model="unicef_supporting_sectors"
              v-validate="rules.unicef_supporting_sectors"
              data-vv-name="unicef_supporting_sectors"
              data-vv-as="UNICEF Supporting Sectors"
              source="getSupportingSectors"
            />
            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>
                  UNICEF's programmes emphasize developing community-level services to promote the health and well-being
                  of children via interventions in health, child protection, social policy, education etc. An initiative
                  is cross-sectoral if it falls in more than one sector or programme area e.g. Introduction of latrines
                  in schools falls in both WASH as well as Education.
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
          <translate key="unicef-goal"> Which Goal Area does the initiative focus on? </translate>
        </template>

        <GoalAreasSelector
          v-model="goal_area"
          v-validate="rules.goal_area"
          data-vv-name="goal_area"
          data-vv-validate-on="change"
          data-vv-as="Goal Area"
        />
        <span class="Hint">
          <fa icon="info-circle" />
          <p>
            <translate>
              Every initiative has a clear, focused goal which is tied to specific results and change strategies to
              achieve them, according to the UNICEF Strategic Plan 2018–2021. The goal is what has to be ultimately
              achieved; the final form or situation that we would like to see. Country work planning activities are
              linked to a single goal area.
            </translate>
          </p>
        </span>
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('result_area')"
        :draft-rule="draftRules.result_area"
        :publish-rule="publishRules.result_area"
      >
        <template slot="label">
          <translate key="result-area"> Which Result Area does the initiative serve? </translate>
        </template>

        <ResultAreasSelector
          v-model="result_area"
          v-validate="rules.result_area"
          :goal-area="goal_area"
          data-vv-name="result_area"
          data-vv-validate-on="change"
          data-vv-as="Result Area"
        />

        <span class="Hint">
          <fa icon="info-circle" />
          <p>
            <translate>
              Every Goal Area is tied to Result Areas, which target the key barriers that hold children and young people
              back, deny them the agency to shape their destinies and prevent them from accessing critical services that
              can save their lives and help them fulfil their potential.
            </translate>
          </p>
        </span>
      </custom-required-form-item>

      <template v-if="shoDHAFields">
        <custom-required-form-item
          :error="errors.first('strategies')"
          :draft-rule="draftRules.strategies"
          :publish-rule="publishRules.strategies"
          class="DigitalHealthIntervention"
        >
          <template slot="label">
            <translate key="strategies"> What are the Digital Health Intervention(s)? </translate>
            <a
              class="TooltipLink"
              target="_blank"
              href="https://apps.who.int/iris/bitstream/handle/10665/260480/WHO-RHR-18.06-eng.pdf;jsessionid=50B83CAF6ACF46453B7D6BAB9672EB77?sequence=1)"
            >
              <fa icon="question-circle" />
            </a>
          </template>
          <digital-health-interventions-selector
            v-validate="rules.strategies"
            data-vv-name="strategies"
            data-vv-as="Digital health interventions"
          />
        </custom-required-form-item>

        <custom-required-form-item
          :error="errors.first('health_focus_areas')"
          :draft-rule="draftRules.health_focus_areas"
          :publish-rule="publishRules.health_focus_areas"
        >
          <template slot="label">
            <translate key="health-focus-areas"> Which Focus Area(s) are addressed by the initiative? </translate>
          </template>
          <template slot="tooltip">
            <el-tooltip
              class="item"
              content="If you encounter an error and/or can not locate the entry
              you would like to see in this list, please send a request with details to invent@unicef.org "
              placement="right"
            >
              <i class="el-icon-warning warning" />
            </el-tooltip>
          </template>

          <health-focus-areas-selector
            v-model="health_focus_areas"
            v-validate="rules.health_focus_areas"
            data-vv-name="health_focus_areas"
            data-vv-validate-on="change"
            data-vv-as="Health focus areas"
          />
          <span class="Hint">
            <fa icon="info-circle" />
            <p>
              <translate>
                Choose relevant entries from the list to help classify your initiative by topic/focus area.
              </translate>
            </p>
          </span>
        </custom-required-form-item>

        <custom-required-form-item
          :error="errors.first('hsc_challenges')"
          :draft-rule="draftRules.hsc_challenges"
          :publish-rule="publishRules.hsc_challenges"
        >
          <template slot="label">
            <translate key="hsc-challenges"> What are the System Challenges addressed by the intervention? </translate>
          </template>
          <template slot="tooltip">
            <el-tooltip
              class="item"
              content="For example, one may implement a digital health intervention,
              such as “targeted communication to clients”, in order to address a
              health system challenge, such as “lack of service utilisation,”
              to achieve an overarching digital health outcome of “improving clients’
              access to knowledge resources and support for better management of their health”."
              placement="right"
            >
              <i class="el-icon-warning warning" />
            </el-tooltip>
          </template>
          <health-system-challenges-selector
            v-model="hsc_challenges"
            v-validate="rules.hsc_challenges"
            data-vv-name="hsc_challenges"
            data-vv-validate-on="change"
            data-vv-as="Health system challenges"
          />
          <span class="Hint">
            <fa icon="info-circle" />
            <p>
              <translate>
                The System Challenge framework provides an overview of needs and challenges faced, and assists programme
                planners to express what they expect to achieve through implementation of a digital intervention. For
                more info: https://uni.cf/invent-help
              </translate>
            </p>
          </span>
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
        <custom-required-form-item v-if="selectedGoalArea.capability_category_question !== 'MISSING'">
          <template slot="label">
            {{ selectedGoalArea.capability_category_question }}
          </template>
          <CapabilitySelector
            v-model="capability_categories"
            :goal-area="goal_area"
            :values-function="getCapabilityCategoriesItems"
          />
        </custom-required-form-item>
        <custom-required-form-item v-if="selectedGoalArea.capability_subcategory_question !== 'MISSING'">
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
              <translate key="priorities-label"> What regional priorities are addressed by the initiative? </translate>
            </template>
            <template slot="tooltip">
              <el-tooltip
                class="item"
                content="Global initiatives can simply leave this field blank."
                placement="right"
              >
                <i class="el-icon-warning warning" />
              </el-tooltip>
            </template>
            <multi-selector
              v-model="regional_priorities"
              v-validate="rules.regional_priorities"
              data-vv-name="regional_priorities"
              data-vv-as="Regional Priorities"
              source="getRegionalPriorities"
              :filter="officeRegion"
            />
            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>
                  For field based initiatives, regions identify their own regional priorities designed to capture the
                  key activities being pursued to address regional development issues and needs.
                </translate>
              </p>
            </span>
          </custom-required-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20" type="flex">
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('innovation_ways')"
            :draft-rule="draftRules.innovation_ways"
            :publish-rule="publishRules.innovation_ways"
          >
            <template slot="label">
              <translate key="ways-label">
                If this is an innovation initiative, in which way is it innovative?
              </translate>
            </template>
            <multi-selector
              v-model="innovation_ways"
              v-validate="rules.innovation_ways"
              data-vv-name="innovation_ways"
              data-vv-as="Innovation"
              source="getInnovationWays"
            />
            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>
                  Innovation can be defined as a new or significantly improved solution that accelerates a result for
                  children or young people and/or increased organizational efficiency.
                </translate>
              </p>
            </span>
          </custom-required-form-item>
        </el-col>
      </el-row>
      <el-row v-show="!hideInnovationCategories" :gutter="20" type="flex">
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('innovation_categories')"
            :draft-rule="draftRules.innovation_categories"
            :publish-rule="publishRules.innovation_categories"
          >
            <template slot="label">
              <translate key="priorities-label">
                Please select all UNICEF Innovation categories this initiative applies to.
              </translate>
            </template>

            <multi-selector
              v-model="innovation_categories"
              v-validate="rules.innovation_categories"
              data-vv-name="innovation_categories"
              data-vv-as="Innovation Categories"
              source="getInnovationCategories"
            />
            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>
                  For more info and definitions of the UNICEF Innovation categories visit: https://uni.cf/invent-help
                </translate>
              </p>
            </span>
          </custom-required-form-item>
        </el-col>
      </el-row>
    </collapsible-card>
  </div>
</template>

<script>
import find from 'lodash/find'
import { mapGetters, mapState } from 'vuex'
import { mapGettersActions } from '@/utilities/form'
// components
import MultiSelector from '@/components/project/MultiSelector'
import MultiSelectorPlatform from '../MultiSelectorPlatform.vue'
import HealthSystemChallengesSelector from '@/components/project/HealthSystemChallengesSelector'
import HealthFocusAreasSelector from '@/components/project/HealthFocusAreasSelector'
import GoalAreasSelector from '@/components/common/GoalAreasSelector'
import ResultAreasSelector from '@/components/common/ResultAreasSelector'
import CapabilitySelector from '@/components/project/CapabilitySelector'
import DigitalHealthInterventionsSelector from '@/components/project/DigitalHealthInterventionsSelector'
import CollapsibleCard from '@/components/project/CollapsibleCard'
// mixins
import ProjectFieldsetMixin from '@/components/mixins/ProjectFieldsetMixin'
import VeeValidationMixin from '@/components/mixins/VeeValidationMixin'

export default {
  components: {
    CollapsibleCard,
    MultiSelector,
    HealthSystemChallengesSelector,
    HealthFocusAreasSelector,
    GoalAreasSelector,
    ResultAreasSelector,
    CapabilitySelector,
    DigitalHealthInterventionsSelector,
    MultiSelectorPlatform,
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  computed: {
    ...mapState({
      offices: (state) => state.offices.offices,
    }),
    ...mapGetters({
      modified: 'project/getModified',
      selectedGoalArea: 'project/getGoalAreaDetails',
      getCapabilityLevelsItems: 'projects/getCapabilityLevels',
      getCapabilityCategoriesItems: 'projects/getCapabilityCategories',
      getCapabilitySubcategoriesItems: 'projects/getCapabilitySubcategories',
      country_office: 'project/getCountryOffice',
      innovationWays: 'projects/getInnovationWays',
    }),
    ...mapGettersActions({
      goal_area: ['project', 'getGoalArea', 'setGoalArea', 0],
      result_area: ['project', 'getResultArea', 'setResultArea', 0],
      capability_levels: ['project', 'getCapabilityLevels', 'setCapabilityLevels', 0],
      capability_categories: ['project', 'getCapabilityCategories', 'setCapabilityCategories', 0],
      capability_subcategories: ['project', 'getCapabilitySubcategories', 'setCapabilitySubcategories', 0],
      health_focus_areas: ['project', 'getHealthFocusAreas', 'setHealthFocusAreas', 0],
      hsc_challenges: ['project', 'getHscChallenges', 'setHscChallenges', 0],
      unicef_sector: ['project', 'getSectors', 'setSectors', 0],
      unicef_leading_sector: ['project', 'getLeadingSector', 'setLeadingSector', 0],
      unicef_supporting_sectors: ['project', 'getSupportingSectors', 'setSupportingSectors', 0],
      regional_priorities: ['project', 'getRegionalPriorities', 'setRegionalPriorities', 0],
      innovation_ways: ['project', 'getInnovationWays', 'setInnovationWays', 0],
      innovation_categories: ['project', 'getInnovationCategories', 'setInnovationCategories', 0],
      platforms: ['project', 'getPlatforms', 'setPlatforms', 0],
    }),
    shoDHAFields() {
      return this.goal_area === 1
    },
    hideInnovationCategories() {
      const na = find(this.innovationWays, ({ name }) => name === 'N/A')
      return na && this.innovation_ways.includes(na.id)
    },
    officeRegion() {
      const office = find(this.offices, ({ id }) => this.country_office === id)
      return office ? office.region : null
    },
  },
  watch: {
    hideInnovationCategories(hide) {
      if (hide) {
        this.innovation_categories = []
      }
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
        this.$validator.validate('unicef_leading_sector'),
        this.$validator.validate('unicef_supporting_sectors'),
        this.$validator.validate('regional_priorities'),
        this.$validator.validate('innovation_categories'),
      ])
      return validations.reduce((a, c) => a && c, true)
    },
  },
}
</script>

<style lang="less"></style>
