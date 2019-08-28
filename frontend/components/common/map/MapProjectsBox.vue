<template>
  <transition name="el-zoom-in-top">
    <div
      v-if="showMapProjectBox"
      class="MapProjectBox"
    >
      <el-row
        type="flex"
        class="CountryHeader"
      >
        <el-col>
          <country-item :id="activeCountry" />
        </el-col>
      </el-row>
      <div
        class="CountrySubHeader"
      >
        <div v-if="showNational">
          <span class="SubLevelItem" />
          <span class="SubLevelCounter">
            <translate :parameters="{count: nationalProjects.length} ">
              &nbsp; {count} project(s)
            </translate>
          </span>
        </div>
      </div>
      <!-- -->
      <el-row class="ProjectsList">
        <el-col>
          <div
            v-show="showSubLevelHint"
            class="HintText"
          >
            <fa
              icon="info-circle"
              size="lg"
            />
            <translate>Click on the map to view the digital health project information.</translate>
          </div>

          <div
            v-show="showNoProjectToShow"
            class="HintText"
          >
            <fa
              icon="info-circle"
              size="lg"
            />
            <translate>No project to show...</translate>
          </div>

          <div
            v-if="showSubNational"
            class="PlainList SubNational"
          >
            <project-card
              v-for="p in currentSubLevelProjects"
              :key="p.id"
              :project="p"
              show-organisation
              show-arrow-on-over
            />
          </div>
          <div
            v-if="showNational"
            class="PlainList National"
          >
            <project-card
              v-for="p in nationalProjects"
              :key="p.id"
              :project="p"
              show-organisation
              show-arrow-on-over
            />
          </div>
        </el-col>
      </el-row>

      <el-button
        circle
        class="CloseBox CancelButton"
        @click="closeCountryProjextBox"
      >
        <fa icon="times" />
      </el-button>
    </div>
  </transition>
</template>

<script>
import CountryItem from '../CountryItem';
import ProjectCard from '../ProjectCard';

export default {
  components: {
    CountryItem,
    ProjectCard
  },
  props: {
    selectedCountry: {
      type: Number,
      default: null
    },
    activeCountry: {
      type: Number,
      default: null
    },
    activeTab: {
      type: String,
      required: true
    },
    activeSubLevel: {
      type: String,
      default: null
    },
    currentSubLevelProjects: {
      type: Array,
      default: () => []
    },
    filteredProjects: {
      type: Array,
      default: () => []
    },
    nationalProjects: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    showTabbedView () {
      return this.activeCountry && !this.selectedCountry;
    },
    showSubNational () {
      return false;
    },
    showNational () {
      return true;
    },
    showSubLevelHint () {
      return false;
    },
    showMapProjectBox () {
      return this.activeCountry;
    },
    showNoProjectToShow () {
      return (this.showNational && this.nationalProjects.length === 0) || (this.showSubNational && this.currentSubLevelProjects.length === 0);
    }
  },
  methods: {
    closeCountryProjextBox () {
      this.$emit('update:activeCountry', null);
    },
    tabChangeHandler (tab) {
      this.$emit('update:activeTab', tab.name);
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .MapProjectBox {
    z-index: 400;
    position: absolute;
    top: 40px;
    left: 40px;
    box-sizing: border-box;
    width: 360px;
    height: auto;
    // TODO
    // max-height: 420px;
    color: @colorWhite;
    background: fade(@colorGrayLightest, 90%);
    box-shadow: 5px 5px 20px 0 rgba(0,0,0,0.15);

    .CountryHeader {
      padding: 20px 20px 0;
      background-color: @colorWhite;
    }

    .CountrySubHeader {
      background-color: @colorWhite;
      padding: 12px 20px 4px;
      border-bottom: 2px solid @colorGrayLight;

      .SubLevelItem {
        display: inline-block;
        width: auto;
        padding-bottom: 8px;
        font-size: @fontSizeBase;
        font-weight: 700;
        color: @colorTextPrimary;
      }

      .SubLevelCounter {
        float: right;
        margin-top: 2px;
        font-size: @fontSizeSmall;
        font-weight: 400;
        color: @colorTextMuted;
      }
    }

    .ProjectsList {
      max-height: 475px;
      overflow: scroll;

      .el-tabs__header {
        margin: 0;
        background-color: @colorWhite;

        .el-tabs__nav-wrap {
          padding: 0 20px;
        }
      }

      .el-tabs__item {
        // Changes to this padding value will require a change on the JS too.
        padding: 0 12px;
      }

      .el-tabs__content,
      .PlainList {
        .ProjectCard {
          margin: 0 10px 8px;

          &:first-child  {
            margin-top: 8px;
          }
        }
      }
    }

    .HintText {
      display: inline-flex;
      align-items: flex-start;
      box-sizing: border-box;
      width: 100%;
      margin: 0;
      padding: 16px 20px;
      background-color: @colorWhite;
      font-size: @fontSizeSmall;
      line-height: 18px;
      color: @colorTextSecondary;

      .svg-inline--fa {
        margin-right: 6px;
        color: @colorTextMuted;
      }
    }

    .CloseBox {
      position: absolute;
      top: 8px;
      right: 8px;
      width: 40px;
      height: 40px;
      color: @colorTextSecondary;
      border: none !important;
      background-color: @colorWhite !important;
      transition: @transitionAll;

      &:hover {
        color: lighten(@colorTextSecondary, 10%) !important;
      }
    }
  }

</style>
