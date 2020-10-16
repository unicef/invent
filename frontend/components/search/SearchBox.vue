<template>
  <div class="search-box">
    <el-row type="flex">
      <el-col>
        <el-input
          :value="q"
          :placeholder="$gettext('Type something...') | translate"
          @input="handleSearch('q', $event)"
        >
          <fa slot="prepend" icon="search" />
        </el-input>
      </el-col>
    </el-row>
    <el-row type="flex" class="search-options">
      <el-col class="search-options-header">
        <el-button
          type="text"
          size="small"
          class="MutedButton IconRight"
          @click="toggleOptionsVisibility"
        >
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
          popper-class="search-box-tooltip"
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
        <el-col v-show="optionsVisible" class="search-options-body">
          <el-checkbox-group
            v-model="searchIn"
            class="OnePerRow CheckboxSmall"
            @change="handleSearch('in', $event)"
          >
            <el-checkbox
              v-for="checkbox in checkboxes"
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
import { mapState, mapMutations, mapActions } from 'vuex'
import debounce from 'lodash/debounce'

export default {
  data() {
    return {
      optionsVisible: false,
      showSearchBoxTooltip: false,
      searchIn: ['name', 'org', 'country', 'overview', 'loc'],
      checkboxes: [
        { label: 'name', text: this.$gettext('Initiative Name') },
        { label: 'org', text: this.$gettext('Organisation') },
        { label: 'country', text: this.$gettext('Country') },
        {
          label: 'overview',
          text: this.$gettext('Overview of the digital health'),
        },
        { label: 'loc', text: this.$gettext('Location') },
      ],
    }
  },
  computed: {
    ...mapState({
      q: (state) => state.search.filter.q,
      in: (state) => state.search.filter.in,
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
    toggleOptionsVisibility() {
      this.optionsVisible = !this.optionsVisible
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.search-box {
  .search-options {
    flex-direction: column;

    .search-options-header {
      margin: 12px 0 0;
      display: flex;
      justify-content: space-between;
      align-items: center;

      .el-button--text {
        padding: 0;
      }

      .MutedButton {
        color: @colorBrandGrayDark;
      }

      .el-tooltip {
        float: right;
        margin-top: 2px;
      }
    }

    .search-options-body {
      margin-top: 5px;

      .el-checkbox {
        margin: 5px 0 0;
        padding: 0;
      }
    }
  }

  .el-input.el-input-group .el-input-group__append,
  .el-input.el-input-group .el-input-group__prepend {
    color: #777779;
    background-color: #f9f8f5;
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

.search-box-tooltip {
  max-width: @advancedSearchWidth;
}
</style>
