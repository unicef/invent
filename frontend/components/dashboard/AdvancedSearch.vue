<template>
  <div class="AdvancedSearch">
    <filter-presets-actions />
    <search-box />
    <country-filters />
    <div class="UnicefSingleSelection">
      <multi-selector
        v-model="unicefSectors"
        class="MultiSelectorFilter"
        source="getSectors"
        :placeholder="$gettext('Unicef Sectors') | translate"
      />
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
        v-model="regionalPriorities"
        class="MultiSelectorFilter"
        source="getRegionalPriorities"
        :placeholder="$gettext('Regional Priorities') | translate"
        :filter="regionalPrioritiesFilter"
      />
      <multi-selector
        v-model="innovationWays"
        class="MultiSelectorFilter"
        source="getInnovationWays"
        :placeholder="$gettext('Innovation Ways') | translate"
      />
      <multi-selector
        v-show="!hideInnovationCategories"
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
    <div>
      <multi-selector
        v-model="phaseOfInitiative"
        :placeholder="$gettext('Phase of Initiative') | translate"
        source="getStages"
        class="MultiSelectorFilter AddMargin"
      />
      <multi-selector
        v-model="hardwarePlatforms"
        class="MultiSelectorFilter AddMargin"
        source="getHardware"
        :placeholder="$gettext('Hardware Platforms') | translate"
      />
      <multi-selector
        v-model="programmePlatforms"
        class="MultiSelectorFilter AddMargin"
        source="getNontech"
        :placeholder="
          $gettext('Programme Innovation/Non-Technology Platforms') | translate
        "
      />
      <multi-selector
        v-model="platformFunctions"
        class="MultiSelectorFilter AddMargin"
        source="getFunctions"
        :placeholder="$gettext('Platform/Product Function') | translate"
      />
      <multi-selector
        v-model="informationSecurity"
        class="MultiSelectorFilter AddMargin"
        source="getInfoSec"
        :placeholder="
          $gettext('Information Security Classification as per Classi')
            | translate
        "
      />
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
import { mapMutations, mapGetters } from 'vuex'
import find from 'lodash/find'

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
      regionalPrioritiesList: 'projects/getRegionalPriorities',
      innovationWaysList: 'projects/getInnovationWays',
      region: 'dashboard/getFilteredRegion',
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
      unicefSectors: ['dashboard', 'getUnicefSectors', 'setUnicefSectors', 0],
      innovationCategories: [
        'dashboard',
        'getInnovationCategories',
        'setInnovationCategories',
        0,
      ],
      regionalPriorities: [
        'dashboard',
        'getRegionalPriorities',
        'setRegionalPriorities',
        0,
      ],
      innovationWays: [
        'dashboard',
        'getInnovationWays',
        'setInnovationWays',
        0,
      ],
      phaseOfInitiative: ['dashboard', 'getPhase', 'setPhase', 0],
      programmePlatforms: [
        'dashboard',
        'getProgrammePlatforms',
        'setProgrammePlatforms',
        0,
      ],
      platformFunctions: [
        'dashboard',
        'getPlatformFunctions',
        'setPlatformFunctions',
        0,
      ],
      informationSecurity: [
        'dashboard',
        'getInformationSecurity',
        'setInformationSecurity',
        0,
      ],
      hardwarePlatforms: [
        'dashboard',
        'getHardwarePlatforms',
        'setHardwarePlatforms',
        0,
      ],
    }),
    regionalPrioritiesFilter() {
      if (this.region === null) {
        return null
      }
      return this.regionalPrioritiesList
        .filter(({ region }) => region === this.region)
        .map(({ id }) => id)
    },
    selectedGoalAreaDetails() {
      if (this.selectedGoal) {
        return this.goalAreas.find((g) => g.id === this.selectedGoal)
      }
      return null
    },
    hideInnovationCategories() {
      const na = find(this.innovationWaysList, ({ name }) => name === 'N/A')
      return na && this.innovationWays.includes(na.id)
    },
  },
  watch: {
    hideInnovationCategories(hide) {
      if (hide) {
        this.innovationCategories = []
      }
    },
  },
  mounted() {
    this.setValue({ key: 'tabs', val: false })
  },
  methods: {
    ...mapMutations({
      setValue: 'filters/SET_VALUE',
    }),
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
  .AddMargin {
    margin-bottom: 12px;
  }
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
