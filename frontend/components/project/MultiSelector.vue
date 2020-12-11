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
    />
  </lazy-el-select>
</template>

<script>
import find from 'lodash/find'
export default {
  name: 'MultiSelector',
  model: {
    prop: 'platforms',
    event: 'change',
  },
  $_veeValidate: {
    value() {
      return this.platform
    },
  },
  props: {
    platforms: {
      type: Array,
      default: () => [],
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
    filter: {
      type: [Array, Number],
      default: null,
    },
  },
  computed: {
    sourceList() {
      const list = this.$store.getters['projects/' + this.source] || []
      if (this.filter === null) {
        return list
      }
      if (this.filter && this.filter.length) {
        return list.filter(({ id }) => this.filter.includes(id))
      }
      return list.filter(({ region }) => region === this.filter)
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
      this.$emit('change', value)
    },
  },
}
</script>

<style lang="less">
//@import "../../assets/style/variables.less";
//@import "../../assets/style/mixins.less";

.PlatformSelector {
  width: 100%;
}
</style>
