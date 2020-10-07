<template>
  <SafeDatePicker
    v-model="internalValue"
    :disabled="disabled"
    class="ImportDatePicker"
    align="center"
    size="small"
  />
</template>

<script>
export default {
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: [String, Date],
      default: null,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    internalValue: {
      get() {
        return this.value instanceof Date ? this.value.toJSON() : this.value
      },
      set(value) {
        this.$emit('change', value ? value.toJSON() : null)
      },
    },
  },
}
</script>

<style lang="less">
.ImportDatePicker {
  &.el-date-editor {
    width: 200px;
  }
}
</style>
