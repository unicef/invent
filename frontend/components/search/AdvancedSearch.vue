<template>
  <div class="advanced-search">
    <filter-presets-actions />
    <search-box />
    <div>
      <!--
      partner -->
      <filter-select
        :value="region"
        :items="regions"
        :placeholder="$gettext('Region') | translate"
        @change="handleSearch('region', $event)"
      />
      <filter-select
        :value="co"
        :items="offices"
        multiple
        :placeholder="$gettext('Country Office') | translate"
        @change="handleSearch('co', $event)"
      />
      <filter-select
        :value="ic"
        :items="innovationCategories"
        multiple
        :placeholder="$gettext('Innovation Category') | translate"
        @change="handleSearch('ic', $event)"
      />
      <!-- <filter-select
        :value="partner"
        :items="partners"
        multiple
        :placeholder="$gettext('Partners') | translate"
        @change="handleSearch('partner', $event)"
      /> -->
      <filter-select
        :value="goal"
        :items="goalAreas"
        multiple
        :placeholder="$gettext('Select Goal Area') | translate"
        @change="handleSearch('goal', $event)"
      />
      <template v-if="portfolioPage === 'portfolio'">
        <filter-select
          :value="sp"
          :items="scalePhases"
          :placeholder="$gettext('Scale Phase') | translate"
          @change="handleSearch('sp', $event)"
        />
        <filter-select
          :value="ps"
          :items="problemStatements"
          multiple
          :placeholder="$gettext('Problem Statement') | translate"
          @change="handleSearch('ps', $event)"
        />
      </template>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'
import debounce from 'lodash/debounce'

import FilterPresetsActions from '@/components/dashboard/FilterPresetsActions'
import SearchBox from '@/components/search/SearchBox'
import FilterSelect from '@/components/search/FilterSelect'

export default {
  components: {
    FilterPresetsActions,
    SearchBox,
    FilterSelect,
  },
  data() {
    return {
      scalePhases: [
        { id: 1, value: '1' },
        { id: 2, value: '2' },
        { id: 3, value: '3' },
        { id: 4, value: '4' },
        { id: 5, value: '5' },
      ],
    }
  },
  computed: {
    ...mapState({
      // prefilter state
      portfolioPage: (state) => state.search.filter.portfolio_page,
      // filters
      region: (state) => state.search.filter.region,
      co: (state) => state.search.filter.co,
      ic: (state) => state.search.filter.ic,
      partner: (state) => state.search.filter.partner,
      goal: (state) => state.search.filter.goal,
      sp: (state) => state.search.filter.sp,
      ps: (state) => state.search.filter.ps,
      // list
      offices: (state) => state.offices.offices,
      problemStatements: (state) => state.portfolio.problemStatements,
    }),

    ...mapGetters({
      goalAreas: 'projects/getGoalAreas',
      regions: 'system/getRegions',
      innovationCategories: 'projects/getInnovationCategories',
      partners: 'project/getPartners',
    }),
  },
  methods: {
    ...mapMutations({
      setSearch: 'search/SET_SEARCH',
    }),
    ...mapActions({
      getSearch: 'search/getSearch',
    }),
    handleSearch(key, val) {
      this.setSearch({ key, val })
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
