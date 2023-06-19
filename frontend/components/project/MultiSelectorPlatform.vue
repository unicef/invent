<template>
  <lazy-el-select
    :value="platforms"
    multiple
    filterable
    :disabled="disabled"
    :placeholder="placeholder || $gettext('Select from list') | translate"
    popper-class="PlatformSelectorDropdown"
    class="PlatformSelector"
    value-key="id"
    @change="changeHandler"
    @blur="$emit('blur')"
  >
    <el-option
      v-for="platform in sourceList"
      :key="platform.id"
      :label="platform.name"
      :value="platform.id"
      :disabled="platform.disabled"
    />
  </lazy-el-select>
</template>

<script>
import find from 'lodash/find'
export default {
  name: 'MultiSelectorPlatform',
  model: {
    prop: 'platforms',
    event: 'change',
  },
  $_veeValidate: {
    value() {
      return this.platforms
    },
  },
  props: {
    platforms: {
      type: Array,
      default: () => [],
    },
    multiple: {
      type: Boolean,
      default: true,
    },
    source: {
      type: String,
      required: true,
    },
    placeholder: {
      type: String,
      default: '',
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    sourceList() {
      return this.$store.getters['projects/' + this.source] || []
    },
  },
  watch: {
    filter(newFilter) {
      if (!this.platforms) {
        return
      }
      let newValue = []
      if (this.filter && this.filter.length !== undefined) {
        newValue = this.platforms.filter((value) => newFilter.includes(value))
      } else {
        newValue = this.platforms.filter((value) => {
          const item = find(this.sourceList, ({ id }) => id === value) || {}
          return item.region === newFilter
        })
      }
      this.changeHandler(newValue)
    },
  },
  methods: {
    changeHandler(value) {
      if (this.multiple === false) {
        this.$emit('change', [value[value.length - 1]])
      } else {
        this.$emit('change', value)
      }
    },
  },
}
</script>

<style lang="less">
.PlatformSelector {
  width: 100%;
}

.AdvancedSearch > div .el-select .el-select__tags::-webkit-scrollbar {
  display: none;
}
.AdvancedSearch > div .el-select .el-select__tags {
  // overflow-x: scroll !important;
}

.el-select .el-select__tags .el-tag__close {
  top: -1px;
  right: 3px;
  margin-right: -5px;
  margin-top: -3px;
  position: sticky;
}
</style>
