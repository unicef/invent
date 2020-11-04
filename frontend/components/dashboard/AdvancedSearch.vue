<template>
  <div class="AdvancedSearch">
    <filter-presets-actions />
    <search-box />
    <country-filters />
    <div class="UnicefSingleSelection">
      <goal-areas-selector
        v-model="selectedGoal"
        :placeholder="$gettext('Goal Area') | translate"
        clearable
      />
      <result-areas-selector
        v-model="selectedResult"
        :goal-area="selectedGoal"
        :placeholder="$gettext('Result Area') | translate"
      />
      <multi-selector
        v-model="innovationCategories"
        class="MultiSelectorFilter"
        source="getInnovationCategories"
        :placeholder="$gettext('Innovation Categories') | translate"
      />
    </div>
    <div class="FilterItems">
      <template v-if="selectedGoal && selectedGoal !== 1">
        <filter-item
          :selected="selectedCapabilityLevels"
          :limit="4"
          :label="selectedGoalAreaDetails.capability_level_question"
          item="capabilityLevels"
        >
          <capability-list
            :value="selectedCapabilityLevels"
            type="capabilityLevels"
            :goal-area="selectedGoal"
            :limit="4"
            actions
            @delete="deleteFromCollection($event, 'selectedCapabilityLevels')"
          />
        </filter-item>
        <filter-item
          :selected="selectedCapabilityCategories"
          :limit="4"
          :label="selectedGoalAreaDetails.capability_category_question"
          item="capabilityCategories"
        >
          <capability-list
            :value="selectedCapabilityCategories"
            type="capabilityCategories"
            :goal-area="selectedGoal"
            :limit="4"
            actions
            @delete="
              deleteFromCollection($event, 'selectedCapabilityCategories')
            "
          />
        </filter-item>
        <filter-item
          :selected="selectedCapabilitySubcategories"
          :limit="4"
          :label="selectedGoalAreaDetails.capability_subcategory_question"
          item="capabilitySubcategories"
        >
          <capability-list
            :value="selectedCapabilitySubcategories"
            type="capabilitySubcategories"
            :goal-area="selectedGoal"
            :limit="4"
            actions
            @delete="
              deleteFromCollection($event, 'selectedCapabilitySubcategories')
            "
          />
        </filter-item>
      </template>
      <template v-if="selectedGoal === 1">
        <filter-item
          :selected="selectedHFA"
          :limit="4"
          :label="$gettext('Health Focus Area') | translate"
          item="hfa"
        >
          <hfa-categories-list
            :value="selectedHFA"
            :limit="4"
            actions
            @delete="deleteFromCollection($event, 'selectedHFA')"
          />
        </filter-item>
        <filter-item
          :selected="selectedHSC"
          :limit="4"
          :label="$gettext('Health System Challenges') | translate"
          item="hsc"
        >
          <health-system-challenges-list
            :value="selectedHSC"
            :limit="4"
            actions
            @delete="deleteFromCollection($event, 'selectedHSC')"
          />
        </filter-item>
        <filter-item
          :selected="selectedDHI"
          :limit="4"
          :label="$gettext('Digital Health Interventions') | translate"
          item="dhi"
        >
          <dhi-categories-list
            :value="selectedDHI"
            :limit="4"
            actions
            @delete="deleteFromCollection($event, 'selectedDHI')"
          />
        </filter-item>
      </template>
      <filter-item
        :selected="selectedPlatforms"
        :limit="4"
        :label="$gettext('Software') | translate"
        item="platform"
      >
        <simple-platform-list
          :value="selectedPlatforms"
          :limit="4"
          actions
          @delete="deleteFromCollection($event, 'selectedPlatforms')"
        />
      </filter-item>
    </div>
  </div>
</template>

<script>
import { mapGettersActions } from '@/utilities/form'

import FilterPresetsActions from '@/components/dashboard/FilterPresetsActions'
import SearchBox from '@/components/dashboard/SearchBox'
import CountryFilters from '@/components/dashboard/CountryFilters'
import FilterItem from '@/components/dashboard/FilterItem'
import DhiCategoriesList from '@/components/common/list/DhiCategoriesList'
import HfaCategoriesList from '@/components/common/list/HfaCategoriesList'
import HealthSystemChallengesList from '@/components/common/list/HealthSystemChallengesList'
import CapabilityList from '@/components/common/list/CapabilityList'
import SimplePlatformList from '@/components/common/list/SimplePlatformList'
import GoalAreasSelector from '@/components/common/GoalAreasSelector'
import ResultAreasSelector from '@/components/common/ResultAreasSelector'
import MultiSelector from '@/components/project/MultiSelector'
import { mapGetters } from 'vuex'

export default {
  components: {
    FilterPresetsActions,
    SearchBox,
    CountryFilters,
    FilterItem,
    DhiCategoriesList,
    HfaCategoriesList,
    HealthSystemChallengesList,
    SimplePlatformList,
    CapabilityList,
    GoalAreasSelector,
    ResultAreasSelector,
    MultiSelector,
  },
  computed: {
    ...mapGetters({
      goalAreas: 'projects/getGoalAreas',
    }),
    ...mapGettersActions({
      selectedGoal: ['dashboard', 'getSelectedGoal', 'setSelectedGoal', 0],
      selectedResult: [
        'dashboard',
        'getSelectedResult',
        'setSelectedResult',
        0,
      ],
      selectedDHI: ['dashboard', 'getSelectedDHI', 'setSelectedDHI', 0],
      selectedHFA: ['dashboard', 'getSelectedHFA', 'setSelectedHFA', 0],
      selectedHSC: ['dashboard', 'getSelectedHSC', 'setSelectedHSC', 0],
      selectedCapabilityLevels: [
        'dashboard',
        'getSelectedCapabilityLevels',
        'setSelectedCapabilityLevels',
        0,
      ],
      selectedCapabilityCategories: [
        'dashboard',
        'getSelectedCapabilityCategories',
        'setSelectedCapabilityCategories',
        0,
      ],
      selectedCapabilitySubcategories: [
        'dashboard',
        'getSelectedCapabilitySubcategories',
        'setSelectedCapabilitySubcategories',
        0,
      ],
      selectedPlatforms: [
        'dashboard',
        'getSelectedPlatforms',
        'setSelectedPlatforms',
        0,
      ],
      innovationCategories: [
        'dashboard',
        'getInnovationCategories',
        'setInnovationCategories',
        0,
      ],
    }),
    selectedGoalAreaDetails() {
      if (this.selectedGoal) {
        return this.goalAreas.find((g) => g.id === this.selectedGoal)
      }
      return null
    },
  },
  methods: {
    deleteFromCollection(id, collectionName) {
      this[collectionName] = this[collectionName].filter((item) => item !== id)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.AdvancedSearch {
  box-sizing: border-box;
  width: @advancedSearchWidth;
  min-height: 100%;
  border-left: 1px solid #eae6e1;
  background-color: @colorWhite;
  > div {
    padding: 21px;
    border-bottom: 1px solid #eae6e1;
    .el-select {
      margin-bottom: 12px;
      .el-select__tags {
        overflow: hidden;
      }
      &:last-child {
        margin-bottom: 0px;
      }
    }
    .el-input {
      .el-input__inner {
        border-color: #a8a8a9;
      }
    }
    &:last-child {
      border: 0;
    }
  }
}
</style>
