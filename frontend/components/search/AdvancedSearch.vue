<template>
  <div class="AdvancedSearch">
    <filter-presets-actions />
    <search-box />
    <!-- <country-filters />
    <div class="UnicefSingleSelection">
      <goal-areas-selector
        v-model="selectedGoal"
        :placeholder="$gettext('Select Goal Area') | translate"
        clearable
      />
      <multi-selector
        v-model="innovationCategories"
        class="MultiSelectorFilter"
        source="getInnovationCategories"
        :placeholder="$gettext('Select Innovation Categories') | translate"
      />
    </div> -->
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { mapGettersActions } from '@/utilities/form'

import FilterPresetsActions from '@/components/dashboard/FilterPresetsActions'
import SearchBox from '@/components/search/SearchBox'
// import CountryFilters from '@/components/dashboard/CountryFilters'
// import GoalAreasSelector from '@/components/common/GoalAreasSelector'
// import MultiSelector from '@/components/project/MultiSelector'

export default {
  components: {
    FilterPresetsActions,
    SearchBox,
    // CountryFilters,
    // GoalAreasSelector,
    // MultiSelector,
  },
  computed: {
    ...mapGetters({
      goalAreas: 'projects/getGoalAreas',
    }),
    ...mapGettersActions({
      // selectedGoal: ['dashboard', 'getSelectedGoal', 'setSelectedGoal', 0],
      // selectedResult: [
      //   'dashboard',
      //   'getSelectedResult',
      //   'setSelectedResult',
      //   0,
      // ],
      // innovationCategories: [
      //   'dashboard',
      //   'getInnovationCategories',
      //   'setInnovationCategories',
      //   0,
      // ],
    }),
    selectedGoalAreaDetails() {
      if (this.selectedGoal) {
        return this.goalAreas.find((g) => g.id === this.selectedGoal)
      }
      return null
    },
  },
  methods: {
    // deleteFromCollection(id, collectionName) {
    //   this[collectionName] = this[collectionName].filter((item) => item !== id)
    // },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.AdvancedSearch {
  box-sizing: border-box;
  width: @advancedSearchWidth;
  // TODO
  min-height: 100%;
  border-left: 1px solid @colorGrayLight;
  background-color: @colorWhite;

  .MultiSelectorFilter {
    margin: 10px 0;
  }
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

  .FilterSwitches {
  }
}
</style>
