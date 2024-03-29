<template>
  <div class="SearchBox">
    <el-row type="flex">
      <el-col>
        <el-input :value="searchString" :placeholder="$gettext('Type something...') | translate" @input="handleSearch">
          <fa slot="prepend" icon="search" />
        </el-input>
      </el-col>
    </el-row>
    <el-row type="flex" class="SearchOptions">
      <el-col class="SearchOptionsHeader">
        <el-button type="text" size="small" class="MutedButton IconRight" @click="toggleOptionsVisibility">
          <translate>Select fields to include in your search</translate>
          <fa v-show="optionsVisible" icon="caret-up" />
          <fa v-show="!optionsVisible" icon="caret-down" />
        </el-button>
        <el-tooltip
          v-model="showSearchBoxTooltip"
          :content="
            $gettext(
              'By selecting these fields, you will limit the search to only data included in these fields. If you want a broader search, leave these fields blank and all project data will be searched.'
            ) | translate
          "
          effect="dark"
          placement="left"
          popper-class="SearchBoxTooltip"
          manual
        >
          <el-button type="text" class="MutedButton" @click="showSearchBoxTooltip = !showSearchBoxTooltip">
            <fa icon="question-circle" />
          </el-button>
        </el-tooltip>
      </el-col>

      <transition name="slide-fade">
        <el-col v-show="optionsVisible" class="SearchOptionsBody">
          <el-checkbox-group v-model="selectedOptions" class="OnePerRow CheckboxSmall">
            <el-checkbox
              v-for="checkbox in searchInOptions"
              :key="checkbox.label"
              :label="checkbox.label"
              class="CheckboxSmall"
            >
              {{ checkbox.text }}
            </el-checkbox>
          </el-checkbox-group>
        </el-col>
      </transition>
    </el-row>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import { mapGettersActions } from '../../utilities/form.js'

export default {
  data() {
    return {
      optionsVisible: false,
      showSearchBoxTooltip: false,
      searchInOptions: [
        { label: 'name', text: this.$gettext('Initiative Name') },
        {
          label: 'overview',
          text: this.$gettext('Overview of the digital health'),
        },
        { label: 'desc', text: this.$gettext('Description') },
        { label: 'ach', text: this.$gettext('Current Achievements') },
        { label: 'partner', text: this.$gettext('Partner Name') },
        { label: 'id', text: this.$gettext('Initiative ID') },
      ],
    }
  },
  computed: {
    ...mapState({
      searchString: (state) => state.dashboard.searchString,
    }),
    ...mapGetters({
      getSearchString: 'dashboard/getSearchString',
    }),
    ...mapGettersActions({
      selectedOptions: ['dashboard', 'getSearchIn', 'setSearchIn', 0],
    }),
  },
  methods: {
    ...mapActions({
      setSearchString: 'dashboard/setSearchString',
    }),
    handleSearch(val) {
      this.setSearchString(val)
    },
    toggleOptionsVisibility() {
      this.optionsVisible = !this.optionsVisible
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.SearchBox {
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
