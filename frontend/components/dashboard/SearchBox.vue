<template>
  <div class="SearchBox">
    <el-row
      type="flex"
      class="SearchInput"
    >
      <el-col>
        <el-input
          v-model="searchString"
          :placeholder="$gettext('Type something...') | translate"
        >
          <fa
            slot="prepend"
            icon="search"
          />
        </el-input>
      </el-col>
    </el-row>
    <el-row
      type="flex"
      class="SearchOptions"
    >
      <el-col class="SearchOptionsHeader">
        <el-button
          type="text"
          size="small"
          class="MutedButton IconRight"
          @click="toggleOptionsVisibility"
        >
          <translate>Select fields to include in your search</translate>
          <fa
            v-show="optionsVisible"
            icon="caret-up"
          />
          <fa
            v-show="!optionsVisible"
            icon="caret-down"
          />
        </el-button>
        <el-tooltip
          v-model="showSearchBoxTooltip"
          :content="$gettext('By selecting these fields, you will limit the search to only data included in these fields. If you want a broader search, leave these fields blank and all project data will be searched.') | translate"
          effect="dark"
          placement="left"
          popper-class="SearchBoxTooltip"
          manual
        >
          <el-button
            type="text"
            class="MutedButton"
            @click="showSearchBoxTooltip = !showSearchBoxTooltip"
          >
            <fa icon="question-circle" />
          </el-button>
        </el-tooltip>
      </el-col>

      <transition name="slide-fade">
        <el-col
          v-show="optionsVisible"
          class="SearchOptionsBody"
        >
          <el-checkbox-group
            v-model="selectedOptions"
            class="OnePerRow CheckboxSmall"
          >
            <el-checkbox
              label="name"
              class="CheckboxSmall"
            >
              <translate>Project Name</translate>
            </el-checkbox>
            <el-checkbox
              label="org"
              class="CheckboxSmall"
            >
              <translate>Organisation Name</translate>
            </el-checkbox>
            <el-checkbox
              label="loc"
              class="CheckboxSmall"
            >
              <translate>Location</translate>
            </el-checkbox>
            <el-checkbox
              label="overview"
              class="CheckboxSmall"
            >
              Overview of the <translate>digital health</translate>
            </el-checkbox>
            <el-checkbox
              label="partner"
              class="CheckboxSmall"
            >
              <translate>Implementing Partners</translate>
            </el-checkbox>
            <el-checkbox
              label="donor"
              class="CheckboxSmall"
            >
              <translate>Investors</translate>
            </el-checkbox>
          </el-checkbox-group>
        </el-col>
      </transition>
    </el-row>
  </div>
</template>

<script>
import { mapGettersActions } from '../../utilities/form.js';

export default {
  data () {
    return {
      optionsVisible: false,
      showSearchBoxTooltip: false
    };
  },
  computed: {
    ...mapGettersActions({
      searchString: ['dashboard', 'getSearchString', 'setSearchString', 300, true],
      selectedOptions: ['dashboard', 'getSearchIn', 'setSearchIn', 0]
    })
  },
  methods: {
    toggleOptionsVisibility () {
      this.optionsVisible = !this.optionsVisible;
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .SearchBox {
    .SearchInput {}

    .SearchOptions {
      flex-direction: column;

      .SearchOptionsHeader {
        margin: 10px 0 0;

        .el-button--text {
          padding: 0;
        }

        .el-tooltip {
          float: right;
          margin-top: 2px;
        }
      }

      .SearchOptionsBody {
        margin-top: 5px;

        .el-checkbox {
          margin: 5px 0 0;
          padding: 0;
        }
      }
    }

    .slide-fade-enter-active {
      transition: @transitionAll;
    }

    .slide-fade-leave-active {
      transition: @transitionAll;
    }

    .slide-fade-enter,
    .slide-fade-leave-to
    /* .slide-fade-leave-active below version 2.1.8 */ {
      transform: translateY(-10px);
      opacity: 0;
    }
  }

  .SearchBoxTooltip {
    max-width: @advancedSearchWidth;
  }
</style>
