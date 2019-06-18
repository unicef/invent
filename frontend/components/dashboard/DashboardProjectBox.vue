<template>
  <div class="DashboardProjectsBox">
    <map-projects-box
      :active-country.sync="activeCountry"
      :active-tab.sync="activeTab"
      :active-sub-level="activeSubLevel"
      :selected-country="selectedCountry"
      :current-sub-level-projects="currentSubNationalProjects"
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
      getActiveCountry: 'dashboard/getActiveCountry',
      selectedCountry: 'dashboard/getSelectedCountry',
      getActiveTab: 'dashboard/getProjectBoxActiveTab',
      activeSubLevel: 'dashboard/getActiveSubLevel',
      currentSubNationalProjects: 'dashboard/getSelectedCountryCurrentSubLevelProjects',
      filteredProjects: 'dashboard/getActiveTabProjects',
      nationalProjects: 'dashboard/getSelectedCountryNationalProjects'
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
      setActiveCountry: 'dashboard/setActiveCountry',
      setActiveTab: 'dashboard/setProjectBoxActiveTab'
    })
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .DashboardProjectsBox {
    .MapProjectBox {
      .el-tabs__content {
        max-height: calc(100vh - @topBarHeight - @actionBarHeight - @appFooterHeight - 156px);
        overflow-y: auto;
      }
    }
  }
</style>
