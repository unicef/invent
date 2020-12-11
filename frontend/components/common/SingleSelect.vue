<template>
  <div>
    <lazy-el-select
      :clearable="clearable"
      :value="realValue"
      :placeholder="placeholder || $gettext('Select from list') | translate"
      popper-class="SelectorPopper"
      class="Selector"
      @change="changeHandler"
    >
      <el-option
        v-for="option in sourceList"
        :key="option.id"
        :label="option.name"
        :value="getValue(option.id)"
      />
    </lazy-el-select>
  </div>
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
      type: [Number, Object],
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
    placeholder: {
      type: String,
      default: '',
    },
    clearable: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    realValue() {
      if (this.clearable) {
        return this.value
      }
      if (this.value === null) {
        return null
      }
      return this.value.toString()
    },
    sourceList() {
      return reject(this.$store.getters[this.source], ({ id }) =>
        this.reject.includes(id)
      )
    },
  },
  methods: {
    getValue(value) {
      return this.clearable ? value : `${value}`
    },
    changeHandler(value) {
      if (this.clearable) {
        this.$emit('change', value || null)
        return
      }
      this.$emit('change', value * 1)
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
