<template>
  <div class="AdvancedSearch">
    <filter-presets-actions />
    <search-box />
    <country-filters />
    <div class="FilterSwitches">
      <filter-switch
        v-model="governamentApproved"
        :label="$gettext('Only MOH Verified Projects') | translate"
        :tooltip="$gettext('Show only projects that have been verified by the country MOH') | translate"
      />
      <filter-switch
        v-model="governamentFinanced"
        :label="$gettext('Government financed') | translate"
        :tooltip="$gettext('Show only projects that have been received financial or in-kind government support') | translate"
      />
    </div>
    <div class="FilterItems">
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
          @delete="deleteDhiHandler"
        />
      </filter-item>
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
          @delete="deleteHfaHandler"
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
          @delete="deleteHscHandler"
        />
      </filter-item>
      <filter-item
        :selected="selectedHIS"
        :limit="4"
        :label="$gettext('Health Information System') | translate"
        item="his"
      >
        <his-bucket-list
          :value="selectedHIS"
          :limit="4"
          actions
          @delete="deleteHisHandler"
        />
      </filter-item>
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
          @delete="deletePlatformsHandler"
        />
      </filter-item>
    </div>
  </div>
</template>

<script>
import { mapGettersActions } from '../../utilities/form';

import FilterPresetsActions from './FilterPresetsActions';
import SearchBox from './SearchBox';
import CountryFilters from './CountryFilters';
import FilterSwitch from './FilterSwitch';
import FilterItem from './FilterItem';
import DhiCategoriesList from '../common/list/DhiCategoriesList';
import HfaCategoriesList from '../common/list/HfaCategoriesList';
import HealthSystemChallengesList from '../common/list/HealthSystemChallengesList';
import HisBucketList from '../common/list/HisBucketList';
import SimplePlatformList from '../common/list/SimplePlatformList';
export default {
  components: {
    FilterPresetsActions,
    SearchBox,
    CountryFilters,
    FilterSwitch,
    FilterItem,
    DhiCategoriesList,
    HfaCategoriesList,
    HealthSystemChallengesList,
    HisBucketList,
    SimplePlatformList
  },
  computed: {
    ...mapGettersActions({
      governamentApproved: ['dashboard', 'getGovernmentApproved', 'setGovernmentApproved', 0],
      governamentFinanced: ['dashboard', 'getGovernmentFinanced', 'setGovernmentFinanced', 0],
      selectedDHI: ['dashboard', 'getSelectedDHI', 'setSelectedDHI', 0],
      selectedHFA: ['dashboard', 'getSelectedHFA', 'setSelectedHFA', 0],
      selectedHSC: ['dashboard', 'getSelectedHSC', 'setSelectedHSC', 0],
      selectedHIS: ['dashboard', 'getSelectedHIS', 'setSelectedHIS', 0],
      selectedPlatforms: ['dashboard', 'getSelectedPlatforms', 'setSelectedPlatforms', 0]
    })
  },
  methods: {
    deleteDhiHandler (id) {
      this.selectedDHI = this.selectedDHI.filter(dhi => dhi !== id);
    },
    deleteHfaHandler (id) {
      this.selectedHFA = this.selectedHFA.filter(hfa => hfa !== id);
    },
    deleteHscHandler (id) {
      this.selectedHSC = this.selectedHSC.filter(hsc => hsc !== id);
    },
    deleteHisHandler (id) {
      this.selectedHIS = this.selectedHIS.filter(his => his !== id);
    },
    deletePlatformsHandler (id) {
      this.selectedPlatforms = this.selectedPlatforms.filter(p => p !== id);
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

    .FilterSwitches {}
  }
</style>
