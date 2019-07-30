<template>
  <div class="AdvancedSearch">
    <filter-presets-actions />
    <search-box />
    <country-filters />
    <div class="UnicefSingleSelection">
      <goal-areas-selector
        v-model="selectedGoal"
        :placeholder="$gettext('Select Goal Area') | translate"
        clearable
      />
      <result-areas-selector
        v-model="selectedResult"
        :goal-area="selectedGoal"
        :placeholder="$gettext('Select Result Area') | translate"
      />
    </div>
    <div class="FilterItems">
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
    </div>
  </div>
</template>

<script>
import { mapGettersActions } from '@/utilities/form';

import FilterPresetsActions from '@/components/dashboard/FilterPresetsActions';
import SearchBox from '@/components/dashboard/SearchBox';
import CountryFilters from '@/components/dashboard/CountryFilters';
import FilterItem from '@/components/dashboard/FilterItem';
import DhiCategoriesList from '@/components/common/list/DhiCategoriesList';
import HfaCategoriesList from '@/components/common/list/HfaCategoriesList';
import HealthSystemChallengesList from '@/components/common/list/HealthSystemChallengesList';
import SimplePlatformList from '@/components/common/list/SimplePlatformList';
import GoalAreasSelector from '@/components/common/GoalAreasSelector';
import ResultAreasSelector from '@/components/common/ResultAreasSelector';

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
    GoalAreasSelector,
    ResultAreasSelector
  },
  computed: {
    ...mapGettersActions({
      selectedGoal: ['dashboard', 'getSelectedGoal', 'setSelectedGoal', 0],
      selectedResult: ['dashboard', 'getSelectedResult', 'setSelectedResult', 0],
      selectedDHI: ['dashboard', 'getSelectedDHI', 'setSelectedDHI', 0],
      selectedHFA: ['dashboard', 'getSelectedHFA', 'setSelectedHFA', 0],
      selectedHSC: ['dashboard', 'getSelectedHSC', 'setSelectedHSC', 0],
      selectedPlatforms: ['dashboard', 'getSelectedPlatforms', 'setSelectedPlatforms', 0]
    })
  },
  methods: {
    deleteFromCollection (id, collectionName) {
      this[collectionName] = this[collectionName].filter(item => item !== id);
    }
  }
};

</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .AdvancedSearch {
    box-sizing: border-box;
    width: @advancedSearchWidth;
    // TODO
    min-height: 100%;
    border-left: 1px solid @colorGrayLight;
    background-color: @colorWhite;

    // search filters blocks
    > div {
      padding: 20px;
      border-bottom: 1px solid @colorGrayLight;

      &:last-child {
        border: 0;
      }
    }

    .UnicefSingleSelection {
      .el-select:first-child {
        margin-bottom: 10px;
      }
    }

    .FilterSwitches {}
  }
</style>
