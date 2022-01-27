<template>
  <div class="advanced-search">
    <filter-presets-actions />
    <search-box />
    <!-- countries -->
    <div class="divider">
      <filter-select
        :value="region"
        :items="regions"
        :placeholder="$gettext('Region') | translate"
        @change="handleSearch('region', $event, regions)"
      />
      <filter-select
        :value="co"
        :items="filteredOffices"
        multiple
        :placeholder="$gettext('UNICEF Office') | translate"
        @change="handleSearch('co', $event, filteredOffices)"
      />
      <filter-select
        :value="country"
        :items="countries"
        :disabled="disabledCountries"
        multiple
        :placeholder="$gettext('Country') | translate"
        @change="handleSearch('country', $event, countries)"
      />
      <filter-select
        :value="ro"
        :items="regionalOffices"
        :disabled="disabledCountries"
        multiple
        :placeholder="$gettext('Multicountry or Regional Office ') | translate"
        @change="handleSearch('ro', $event, regionalOffices)"
      />
    </div>
    <!-- areas -->
    <div class="divider">
      <filter-select
        :value="us"
        :items="sectors"
        multiple
        :placeholder="$gettext('Unicef Sectors') | translate"
        @change="handleSearch('us', $event, sectors)"
      />
      <filter-select
        :value="goal"
        :items="goalAreas"
        :placeholder="$gettext('Goal Area') | translate"
        @change="handleSearch('goal', $event, goalAreas)"
      />
      <filter-select
        :value="result"
        :items="filteredResultAreas"
        :disabled="disabledResultAreas"
        :placeholder="$gettext('Result Area') | translate"
        @change="handleSearch('result', $event, filteredResultAreas)"
      />
      <filter-select
        :value="rp"
        :items="regionalPriorities"
        multiple
        :placeholder="$gettext('Regional Priorities') | translate"
        @change="handleSearch('rp', $event, regionalPriorities)"
      />
      <filter-select
        :value="iw"
        :items="innovationWays"
        multiple
        :placeholder="$gettext('Innovation Ways') | translate"
        @change="handleSearch('iw', $event, innovationWays)"
      />
      <filter-select
        v-if="showIC"
        :value="ic"
        :items="innovationCategories"
        multiple
        :placeholder="$gettext('Innovation Category') | translate"
        @change="handleSearch('ic', $event, innovationCategories)"
      />
    </div>
    <!-- portfolio -->
    <div v-if="portfolioPage === 'portfolio'" class="divider">
      <filter-select
        :value="sp"
        :items="scalePhases"
        :placeholder="$gettext('Scale Phase') | translate"
        @change="handleSearch('sp', $event, scalePhases)"
      />
      <filter-select
        :value="ps"
        :items="problemStatements"
        :placeholder="$gettext('Problem Statement') | translate"
        option-class="statement-options"
        @change="handleSearch('ps', $event, problemStatements)"
      />
    </div>
    <!-- goal dependencies -->
    <div class="divider">
      <template v-if="goal && goal !== 1">
        <filter-item
          :selected="selectedCapabilityLevels"
          :limit="4"
          :label="selectedGoalAreaDetails.capability_level_question"
          item="capabilityLevels"
        >
          <capability-list
            :value="selectedCapabilityLevels"
            type="capabilityLevels"
            :goal-area="goal"
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
            :goal-area="goal"
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
            :goal-area="goal"
            :limit="4"
            actions
            @delete="
              deleteFromCollection($event, 'selectedCapabilitySubcategories')
            "
          />
        </filter-item>
      </template>
      <template v-if="goal === 1">
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
    <!-- platforms and extras -->
    <div class="divider">
      <filter-select
        :value="stage"
        :items="stages"
        multiple
        :placeholder="$gettext('Current Phase of Initiative') | translate"
        @change="handleSearch('stage', $event, stages)"
      />
      <filter-select
        :value="hp"
        :items="hardwares"
        multiple
        :placeholder="$gettext('Hardware Platforms') | translate"
        @change="handleSearch('hp', $event, hardwares)"
      />
      <filter-select
        :value="pp"
        :items="nontechs"
        multiple
        :placeholder="
          $gettext('Programme Innovation/Non-Technology Platforms') | translate
        "
        @change="handleSearch('pp', $event, nontechs)"
      />
      <filter-select
        :value="pf"
        :items="functions"
        multiple
        :placeholder="$gettext('Platform/Product Function') | translate"
        @change="handleSearch('pf', $event, functions)"
      />
      <filter-select
        :value="is"
        :items="classifications"
        multiple
        :placeholder="
          $gettext('Information Security Classification') | translate
        "
        @change="handleSearch('is', $event, classifications)"
      />
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'
import { mapGettersActions } from '@/utilities/form'
import debounce from 'lodash/debounce'

import FilterPresetsActions from '@/components/dashboard/FilterPresetsActions'
import SearchBox from '@/components/search/SearchBox'
import FilterSelect from '@/components/search/FilterSelect'

// dialogs selectors
import FilterItem from '@/components/dashboard/FilterItem'
import DhiCategoriesList from '@/components/common/list/DhiCategoriesList'
import HfaCategoriesList from '@/components/common/list/HfaCategoriesList'
import HealthSystemChallengesList from '@/components/common/list/HealthSystemChallengesList'
import CapabilityList from '@/components/common/list/CapabilityList'
import SimplePlatformList from '@/components/common/list/SimplePlatformList'

export default {
  components: {
    FilterPresetsActions,
    SearchBox,
    FilterSelect,
    // dialogs selectors for goal dependencies
    FilterItem,
    DhiCategoriesList,
    HfaCategoriesList,
    HealthSystemChallengesList,
    CapabilityList,
    SimplePlatformList,
  },
  data() {
    return {
      showIC: true,
    }
  },
  computed: {
    ...mapGettersActions({
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
    }),
    ...mapState({
      // prefilter state
      portfolioPage: (state) => state.search.filter.portfolio_page,
      // filters
      // country
      region: (state) => state.search.filter.region,
      co: (state) => state.search.filter.co,
      country: (state) => state.search.filter.country,
      ro: (state) => state.search.filter.ro,
      // areas
      us: (state) => state.search.filter.us,
      goal: (state) => state.search.filter.goal,
      result: (state) => state.search.filter.result,
      rp: (state) => state.search.filter.rp,
      iw: (state) => state.search.filter.iw,
      ic: (state) => state.search.filter.ic,
      // another
      partner: (state) => state.search.filter.partner,
      sp: (state) => state.search.filter.sp,
      ps: (state) => state.search.filter.ps,
      // list
      offices: (state) => state.offices.offices,
      scalePhases: (state) => state.system.scalePhases,
      problemStatements: (state) => state.portfolio.problemStatements,
      // dialogs
      sw: (state) => state.search.filter.sw,
      dhi: (state) => state.search.filter.dhi,
      hfa: (state) => state.search.filter.hfa,
      hsc: (state) => state.search.filter.hsc,
      cl: (state) => state.search.filter.cl,
      cc: (state) => state.search.filter.cc,
      cs: (state) => state.search.filter.cc,
      // platforms and extras
      stage: (state) => state.search.filter.stage,
      hp: (state) => state.search.filter.hp,
      pp: (state) => state.search.filter.pp,
      pf: (state) => state.search.filter.pf,
      is: (state) => state.search.filter.is,
    }),
    ...mapGetters({
      regions: 'system/getRegions',
      regionalOffices: 'projects/getRegionalOffices',
      countries: 'countries/getCountries',
      goalAreas: 'projects/getGoalAreas',
      resultAreas: 'projects/getResultAreas',
      innovationCategories: 'projects/getInnovationCategories',
      partners: 'project/getPartners',
      sectors: 'projects/getSectors',
      regionalPriorities: 'projects/getRegionalPriorities',
      innovationWays: 'projects/getInnovationWays',
      stages: 'projects/getStages',
      hardwares: 'projects/getHardware',
      nontechs: 'projects/getNontech',
      functions: 'projects/getFunctions',
      classifications: 'projects/getInfoSec',
    }),
    disabledCountries() {
      return !!(this.co && this.co.length > 0 && this.co !== null)
    },
    disabledResultAreas() {
      return this.goal === '' || this.goal === null
    },
    filteredResultAreas() {
      return this.resultAreas.filter((i) => i.goal_area_id === this.goal)
    },
    filteredOffices() {
      if (
        this.region !== '' &&
        this.region !== undefined &&
        this.region !== null
      ) {
        return this.offices.filter(
          (i) => i.region === parseInt(this.region, 10)
        )
      }
      return this.offices
    },
    selectedGoalAreaDetails() {
      if (this.goal) {
        return this.goalAreas.find((g) => g.id === this.goal)
      }
      return null
    },
  },
  watch: {
    region(newRegion) {
      this.handleSearch(
        'country',
        Number.isInteger(newRegion)
          ? this.country.filter((c) => c.unicef_region === newRegion.id)
          : this.country
      )
    },
    co(newOffices) {
      if (newOffices.length > 0) {
        this.setSearch({ key: 'ro', val: [14] })
      } else {
        this.setSearch({ key: 'ro', val: [] })
      }
      this.handleSearch(
        'country',
        Array.isArray(newOffices)
          ? this.offices
              .filter((o) => newOffices.includes(o.id))
              .map((c) => c.country)
          : this.offices
              .filter((o) => newOffices === o.id)
              .map((c) => c.country)
      )
    },
    goal(newGoal) {
      if (newGoal === '' || newGoal === null) {
        this.handleSearch('result', '')
      }
    },
    selectedPlatforms() {
      this.handleSearch('sw', this.selectedPlatforms)
    },
    selectedDHI() {
      this.handleSearch('dhi', this.selectedDHI)
    },
    selectedHFA() {
      this.handleSearch('hfa', this.selectedHFA)
    },
    selectedHSC() {
      this.handleSearch('hsc', this.selectedHSC)
    },
    selectedCapabilityLevels() {
      this.handleSearch('cl', this.selectedCapabilityLevels)
    },
    selectedCapabilityCategories() {
      this.handleSearch('cc', this.selectedCapabilityCategories)
    },
    selectedCapabilitySubcategories() {
      this.handleSearch('cs', this.selectedCapabilitySubcategories)
    },
    iw(niw) {
      if (niw.includes(1)) {
        this.setSearch({ key: 'ic', val: [] })
        this.showIC = false
      } else {
        this.showIC = true
      }
    },
  },
  mounted() {
    this.setBlockSearch(false)
    this.setValue({ key: 'tabs', val: true })
  },
  beforeDestroy() {
    this.setBlockSearch(true)
  },
  methods: {
    ...mapMutations({
      setSearch: 'search/SET_SEARCH',
      setValue: 'filters/SET_VALUE',
    }),
    ...mapActions({
      getSearch: 'search/getSearch',
      setBlockSearch: 'search/setBlockSearch',
    }),
    deleteFromCollection(id, collectionName) {
      this[collectionName] = this[collectionName].filter((item) => item !== id)
    },
    handleSearch(key, val, items) {
      const target = items ? items.find((i) => i.name === 'N/A') : undefined
      if (target !== undefined && val.includes(target.id)) {
        this.setSearch({ key, val: [target.id] })
      } else {
        this.setSearch({ key, val })
      }
      this.getSearchResults()
    },
    getSearchResults: debounce(function () {
      this.getSearch()
    }, 350),
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.advanced-search {
  box-sizing: border-box;
  width: @advancedSearchWidth;
  min-height: 100%;
  border-left: 1px solid #eae6e1;
  background-color: @colorWhite;
  > div {
    padding: 20px;
    border-bottom: 1px solid #eae6e1;
    .el-select {
      margin-bottom: 12px;
      &:last-child {
        margin-bottom: 0;
      }
      .el-select__tags {
        overflow: hidden;
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
