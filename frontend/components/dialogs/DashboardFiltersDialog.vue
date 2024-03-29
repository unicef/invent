<template>
  <el-dialog
    v-if="visible"
    :visible.sync="visible"
    :title="$gettext('Applying specific filter to map/list') | translate"
    modal
    top="10vh"
    width="90vw"
    custom-class="FilterDialog"
    @opened="loadCurrentSelection"
  >
    <el-row type="flex" class="FilterDialogWrapper">
      <el-col class="FilterSelector">
        <template v-if="selectedGoalArea === 1">
          <filter-item
            :active="selectedFilter === 'dhi'"
            :selected="dhi"
            :header="$gettext('Digital Health Interventions') | translate"
            item="dhi"
            @clear="dhi = []"
          />
          <filter-item
            :active="selectedFilter === 'hfa'"
            :selected="hfa"
            :header="$gettext('Health focus areas') | translate"
            item="hfa"
            @clear="hfa = []"
          />
          <filter-item
            :active="selectedFilter === 'hsc'"
            :selected="hsc"
            :header="$gettext('Health system challenges') | translate"
            item="hsc"
            @clear="hsc = []"
          />
        </template>
        <template v-else-if="selectedGoalAreaDetails">
          <filter-item
            :active="selectedFilter === 'capabilityLevels'"
            :selected="capabilityLevels"
            :header="selectedGoalAreaDetails.capability_level_question"
            item="capabilityLevels"
            @clear="capabilityLevels = []"
          />
          <filter-item
            :active="selectedFilter === 'capabilityCategories'"
            :selected="capabilityCategories"
            :header="selectedGoalAreaDetails.capability_category_question"
            item="capabilityCategories"
            @clear="capabilityCategories = []"
          />
          <filter-item
            :active="selectedFilter === 'capabilitySubcategories'"
            :selected="capabilitySubcategories"
            :header="selectedGoalAreaDetails.capability_subcategory_question"
            item="capabilitySubcategories"
            @clear="capabilitySubcategories = []"
          />
        </template>
        <filter-item
          :active="selectedFilter === 'platform'"
          :selected="platforms"
          :header="$gettext('Software')"
          item="platform"
          @clear="platforms = []"
        />
      </el-col>
      <el-col class="FilterArea">
        <digital-health-interventions-filter
          v-show="selectedFilter === 'dhi'"
          :selected.sync="dhi"
        />
        <health-focus-areas-filter
          v-show="selectedFilter === 'hfa'"
          :selected.sync="hfa"
        />
        <health-system-challenges-filter
          v-show="selectedFilter === 'hsc'"
          :selected.sync="hsc"
        />
        <platform-filter
          v-show="selectedFilter === 'platform'"
          :selected.sync="platforms"
        />
        <template v-if="selectedGoalArea && selectedGoalArea !== 1">
          <capability-filter
            v-show="selectedFilter === 'capabilityLevels'"
            type="capabilityLevels"
            :goal-area="selectedGoalArea"
            :selected.sync="capabilityLevels"
          />
          <capability-filter
            v-show="selectedFilter === 'capabilityCategories'"
            type="capabilityCategories"
            :goal-area="selectedGoalArea"
            :selected.sync="capabilityCategories"
          />
          <capability-filter
            v-show="selectedFilter === 'capabilitySubcategories'"
            type="capabilitySubcategories"
            :goal-area="selectedGoalArea"
            :selected.sync="capabilitySubcategories"
          />
        </template>
      </el-col>
    </el-row>
    <span slot="footer">
      <el-row type="flex" align="center">
        <el-col class="SecondaryButtons">
          <el-button type="text" class="CancelButton" @click="cancel">
            <translate>Cancel</translate>
          </el-button>
        </el-col>
        <el-col class="PrimaryButtons">
          <el-button type="primary" @click="apply">
            <translate>Apply filters</translate>
          </el-button>
        </el-col>
      </el-row>
    </span>
  </el-dialog>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import CapabilityFilter from '@/components/dialogs/filters/CapabilityFilter'
import { mapGettersActions } from '../../utilities/form.js'
import FilterItem from './FilterItem'
import HealthFocusAreasFilter from './filters/HealthFocusAreaFilter'
import DigitalHealthInterventionsFilter from './filters/DigitalHealthInterventionsFilter'

import HealthSystemChallengesFilter from './filters/HealthSystemChallengesFilter'
import PlatformFilter from './filters/PlatformFilter'

export default {
  components: {
    FilterItem,
    HealthFocusAreasFilter,
    DigitalHealthInterventionsFilter,
    HealthSystemChallengesFilter,
    PlatformFilter,
    CapabilityFilter,
  },
  data() {
    return {
      dhi: [],
      hfa: [],
      hsc: [],
      capabilityLevels: [],
      capabilityCategories: [],
      capabilitySubcategories: [],
      platforms: [],
    }
  },
  computed: {
    ...mapGetters({
      selectedFilter: 'layout/getDashboardFiltersDialogState',
      selectedGoalArea: 'dashboard/getSelectedGoal',
      goalAreas: 'projects/getGoalAreas',
    }),
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
    selectedGoalAreaDetails() {
      if (this.selectedGoalArea) {
        return this.goalAreas.find((g) => g.id === this.selectedGoalArea)
      }
      return null
    },
    visible: {
      get() {
        return this.selectedFilter !== null
      },
      set() {
        this.setDashboardFiltersDialogState(null)
      },
    },
  },
  methods: {
    ...mapActions({
      setDashboardFiltersDialogState: 'layout/setDashboardFiltersDialogState',
    }),
    loadCurrentSelection() {
      this.dhi = [...this.selectedDHI]
      this.hfa = [...this.selectedHFA]
      this.hsc = [...this.selectedHSC]
      this.capabilityLevels = [...this.selectedCapabilityLevels]
      this.capabilityCategories = [...this.selectedCapabilityCategories]
      this.capabilitySubCategories = [...this.selectedCapabilitySubcategories]
      this.platforms = [...this.selectedPlatforms]
    },
    clearAll() {
      this.dhi = []
      this.hfa = []
      this.hsc = []
      this.capabilityLevels = []
      this.capabilityCategories = []
      this.capabilitySubcategories = []
      this.platforms = []
    },
    cancel() {
      this.setDashboardFiltersDialogState(null)
    },
    apply() {
      console.log('filter to apply')
      console.log(this.selectedFilter)
      switch (this.selectedFilter) {
        case 'dhi':
          this.selectedDHI = this.dhi
          break
        case 'hfa':
          this.selectedHFA = this.hfa
          break
        case 'hsc':
          this.selectedHSC = this.hsc
          break
        case 'capabilityLevels':
          this.selectedCapabilityLevels = this.capabilityLevels
          break
        case 'capabilityCategories':
          this.selectedCapabilityCategories = this.capabilityCategories
          break
        case 'capabilitySubcategories':
          this.selectedCapabilitySubcategories = this.capabilitySubcategories
          break
        case 'platform':
          this.selectedPlatforms = this.platforms
          break
      }
      this.$nextTick(() => {
        this.setDashboardFiltersDialogState(null)
      })
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.FilterDialog {
  max-width: @appWidthMaxLimit * 0.9;
  height: 80vh;
  margin-top: 0;
  margin-bottom: 0;

  .el-dialog__body {
    padding: 0;
    height: inherit;
    overflow: hidden;
    overflow-y: hidden !important;
  }

  .FilterDialogWrapper {
    height: inherit;

    .FilterSelector {
      position: relative;
      z-index: 2002;
      box-sizing: border-box;
      min-width: @filterSelectorWidth;
      max-width: @filterSelectorWidth;
      background-color: @colorWhite;
      border-right: 2px solid @colorGrayLight;
    }

    .FilterArea {
      width: 100%;

      .Main {
        .SelectorDialogCategory {
          .Items {
            padding-left: 0;
          }
        }
      }
    }

    // Special case for DHI items
    .DigitalHealthInterventionsFilter {
      .el-col-6 {
        overflow: hidden;
        height: inherit;
        border-right: 1px solid @colorGrayLight;

        .SelectorDialogColumn {
          .Header {
            position: relative;
            width: 100%;
            max-width: 100%;
            .el-checkbox__label {
              font-size: 10px;
            }
          }
          .Main {
            top: 0;
            .Item {
              .el-checkbox__label {
                font-size: @fontSizeSmall;
                line-height: 16px;
              }
            }
          }
        }
        &:last-child {
          border: 0;
          .SelectorDialogColumn {
            .Header {
              position: relative;
              width: 100%;
              max-width: 100%;
            }
          }
        }
      }
    }

    .HealthFocusAreaFilter,
    .HealthSystemChallengesFilter,
    .HealthInformationSystem,
    .PlatformFilter {
      .SelectorDialogColumn {
        .Header {
          position: relative;
          width: 100%;
          max-width: 100%;
        }
      }
      .Main {
        top: 0;
        .Items {
          margin: 0;
        }
      }
    }
  }
}
</style>
