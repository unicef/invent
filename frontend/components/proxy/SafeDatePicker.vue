<template>
  <el-date-picker
    v-bind="propsAndAttrs"
    v-on="$listeners"
    @click.native="checkValue(value)"
  />
</template>

<script>
export default {
  name: 'SafeDatePicker',
  props: {
    value: {
      type: null,
      required: true,
    },
  },
  computed: {
    propsAndAttrs() {
      return { ...this.$props, ...this.$attrs }
    },
    listeners() {
      return { ...this.$listeners }
    },
  },
  methods: {
    checkValue(value) {
      if (!(value && value instanceof Date && value.toJSON())) {
        this.$emit('input', null)
      }
    },
  },
}
</script>

<style></style>
