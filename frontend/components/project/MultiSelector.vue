<template>
  <lazy-el-select
    :value="platforms"
    multiple
    :multiple-limit="multipleLimit"
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
    multipleLimit: {
      type: Number,
      default: 0,
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
      // source list logic
      let sourceList
      const fullList = this.$store.getters['projects/' + this.source] || []
      if (this.filter === null) {
        sourceList = fullList
      } else if (this.filter && this.filter.length) {
        sourceList = fullList.filter(({ id }) => this.filter.includes(id))
      } else {
        sourceList = fullList.filter(({ region }) => region === this.filter)
      }
      // disabled list logic
      const targets = this.$store.getters['projects/' + this.source].filter((i) => i.name === 'N/A' || i.name === 'No')
      let target
      targets.forEach((tar) => {
        if (this.platforms.includes(tar.id)) {
          target = tar
        }
      })
      if (target !== undefined && this.platforms.includes(target.id)) {
        sourceList = sourceList.map((i) => {
          if (i.id === target.id) {
            return { ...i, disabled: false }
          }
          return { ...i, disabled: true }
        })
      } else {
        sourceList = sourceList.map((i) => {
          return { ...i, disabled: false }
        })
      }
      return sourceList
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
    platforms(val) {
      const target = this.sourceList.find((i) => i.name === 'N/A')
      if (target !== undefined && val.includes(target.id)) {
        this.platformList = this.sourceList.map((i) => {
          if (i.name === 'N/A') {
            return { ...i, disabled: false }
          }
          return { ...i, disabled: true }
        })
      } else {
        this.platformList = this.sourceList.map((i) => {
          return { ...i, disabled: false }
        })
      }
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
