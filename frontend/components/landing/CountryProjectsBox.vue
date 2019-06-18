<template>
  <div class="CountryProjectsBox">
    <map-projects-box
      :active-country.sync="activeCountry"
      :active-tab.sync="activeTab"
      :active-sub-level="activeSubLevel"
      :selected-country="selectedCountry"
      :current-sub-level-projects="currentSubLevelProjects"
      :filtered-projects="filteredProjects"
      :national-projects="nationalProjects"
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

import MapProjectsBox from '../common/map/MapProjectsBox';

export default {
  components: {
    MapProjectsBox
  },
  props: {
  },
  computed: {
    ...mapGetters({
      getActiveCountry: 'landing/getActiveCountry',
      selectedCountry: 'landing/getSelectedCountry',
      getActiveTab: 'landing/getProjectBoxActiveTab',
      activeSubLevel: 'landing/getActiveSubLevel',
      currentSubLevelProjects: 'landing/getSelectedCountryCurrentSubLevelProjects',
      filteredProjects: 'landing/getActiveTabProjects',
      nationalProjects: 'landing/getSelectedCountryNationalProjects'
    }),
    activeCountry: {
      get () {
        return this.getActiveCountry;
      },
      set (value) {
        this.setActiveCountry(value);
      }
    },
    activeTab: {
      get () {
        return this.getActiveTab;
      },
      set (value) {
        this.setActiveTab(value);
      }
    }
  },
  methods: {
    ...mapActions({
      setActiveCountry: 'landing/setActiveCountry',
      setActiveTab: 'landing/setProjectBoxActiveTab'
    })
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .CountryProjectsBox {
    .MapProjectBox {
      .el-tabs__content {
        max-height: calc(@landingMapHeight - 155px);
        overflow-y: auto;

        @media screen and (max-height: 694px) {
          max-height: calc(@landingMapMinHeight - 155px);
        }
      }
    }
  }

</style>
