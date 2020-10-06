<template>
  <lazy-el-select
    :value="value"
    :placeholder="$gettext('Select investor') | translate"
    popper-class="SelectorPopper"
    class="Selector"
    @change="changeHandler"
  >
    <el-option
      v-for="option in sourceList"
      :key="option.id"
      :label="option.name"
      :value="option.id"
    />
  </lazy-el-select>
</template>

<script>
import reject from 'lodash/reject'
export default {
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: Number,
      default: null,
    },
    source: {
      type: String,
      required: true,
    },
    reject: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    sourceList() {
      return reject(this.$store.getters[this.source], ({ id }) =>
        this.reject.includes(id)
      )
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
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.Selector {
  width: 100%;
}
.SelectorPopper {
  max-width: @advancedSearchWidth - 40px;
}
</style>
