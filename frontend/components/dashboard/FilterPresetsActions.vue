<template>
  <div class="FilterPresets">
    <el-row type="flex" align="middle">
      <el-col :span="12">
        <el-popover
          :title="$gettext('My filters presets') | translate"
          placement="bottom-center"
          popper-class="CustomPopover AdvancedSearchPresetsDropdown"
          trigger="click"
        >
          <el-button slot="reference" type="text" class="IconRight">
            <span v-if="currentFilter"> {{ currentFilter }} </span>
            <translate v-else> Load filters </translate>
            <fa icon="caret-down" />
          </el-button>
          <div class="CustomPopoverList">
            <p v-if="emptyFilters">
              <translate>No Filters saved</translate>
            </p>
            <ul v-else>
              <li
                v-for="(value, name) in filters"
                :key="name"
                :class="{ Active: currentFilter === name }"
                @click="handleFilterSelect(name)"
              >
                <fa icon="check" />
                <el-button
                  type="text"
                  class="DeleteButton"
                  @click.stop="handleDelete(name)"
                >
                  <fa icon="times" />
                </el-button>
                {{ name }}
              </li>
            </ul>
          </div>
        </el-popover>
      </el-col>
      <el-col :span="6">
        <el-button type="text" :disabled="disabled" @click="openSaveFilter">
          <translate>Save</translate>
        </el-button>
      </el-col>
      <el-col :span="6">
        <el-button
          type="text"
          :disabled="disabled"
          :class="disabled ? 'MutedButton' : 'DeleteButton'"
          @click="handleReset"
        >
          <translate>Clear</translate>
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import isEmpty from 'lodash/isEmpty'
import isEqual from 'lodash/isEqual'

import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  data() {
    return {
      emptySearch: {
        q: '',
        // in: ['name', 'org', 'country', 'overview', 'loc'],
        country: [],
        sw: [],
        dhi: [],
        hfa: [],
        hsc: [],
        region: '',
        // partner: [],
        co: [],
        goal: '',
        result: '',
        cl: [],
        cc: [],
        cs: [],
        ic: [],
        sp: '',
        ps: '',
      },
      emptySearchInventory: {
        q: '',
        // in: ['name', 'org', 'country', 'overview', 'loc'],
        country: [],
        sw: [],
        dhi: [],
        hfa: [],
        hsc: [],
        region: '',
        co: [],
        goal: '',
        result: '',
        cl: [],
        cc: [],
        cs: [],
        ic: [],
      },
    }
  },
  computed: {
    ...mapState({
      tabs: (state) => state.filters.tabs,
      filters: (state) => state.filters.filters,
      currentFilter: (state) => state.filters.currentFilter,
      currentSearchFilter: (state) => state.search.filter,
    }),
    ...mapGetters({
      getSearchParameters: 'dashboard/getSearchParameters',
    }),
    emptyFilters() {
      return isEmpty(this.filters)
    },
    disabled() {
      if (this.tabs) {
        return this.isSearchEmpty(this.emptySearch, this.currentSearchFilter)
      } else {
        return this.isSearchEmpty(
          this.emptySearchInventory,
          this.getSearchParameters
        )
      }
    },
  },
  mounted() {
    this.setCurrentFilter()
    this.getFilters()
  },
  methods: {
    ...mapActions({
      setSaveFiltersDialogState: 'layout/setSaveFiltersDialogState',
      getFilters: 'filters/getFilters',
      setCurrentFilter: 'filters/setCurrentFilter',
      setFilters: 'filters/setFilters',
      resetFilters: 'filters/resetFilters',
      deleteFilter: 'filters/deleteFilter',
      getSearch: 'search/getSearch',
    }),
    isSearchEmpty(keys, filter) {
      for (const key in keys) {
        if (!isEqual(filter[key], keys[key])) return false
      }
      return true
    },
    openSaveFilter() {
      this.setSaveFiltersDialogState(true)
    },
    handleReset() {
      this.resetFilters()
      if (this.tabs) {
        this.getSearch()
      }
    },
    handleFilterSelect(name) {
      this.setFilters(name)
    },
    async handleDelete(name) {
      try {
        await this.$confirm(
          this.$gettext(
            'This will permanently delete this saved configuration. Continue?'
          ),
          this.$gettext('Warning'),
          {
            confirmButtonText: this.$gettext('OK'),
            cancelButtonText: this.$gettext('Cancel'),
            type: 'warning',
          }
        )
        await this.deleteFilter(name)
      } catch (e) {
        this.$message(this.$gettext('Operation successfully aborted'))
      }
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.FilterPresets {
  padding: 20px !important;
  background-color: @colorWhite;

  .el-col {
    // Selector
    &:nth-child(1) {
      width: 100%;
    }

    // Save
    &:nth-child(2) {
      width: auto;
      padding-left: 15px;
    }

    // Clear
    &:nth-child(3) {
      width: auto;
      padding-left: 15px;
    }
  }

  .el-button--text {
    padding: 0;
  }
}

.AdvancedSearchPresetsDropdown {
  transform: translate(-10px, -5px);
  max-width: @advancedSearchWidth - 30px;
}
</style>
