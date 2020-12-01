<template>
  <lazy-el-select
    :value="platforms"
    multiple
    filterable
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
    filter: {
      type: Number,
      default: null,
    },
  },
  computed: {
    sourceList() {
      const list = this.$store.getters['projects/' + this.source] || []
      if (this.filter === null) {
        return list
      }
      return list.filter(({ region }) => region === this.filter)
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
