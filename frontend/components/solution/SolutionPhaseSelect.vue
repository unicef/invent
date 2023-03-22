<template>
  <lazy-el-select
    v-model="innerValue"
    :multiple="false"
    :disabled="disabled"
    :placeholder="$gettext('Phase') | translate"
    filterable
    class="select-solution-phase"
  >
    <el-option v-for="solution in solutions" :key="solution.id + 1" :label="solution.name" :value="solution.id + 1" />
  </lazy-el-select>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: Number,
      default: 0,
    },
    disabled: {
      type: Boolean,
      default: false,
      required: false,
    },
    multiple: {
      type: Boolean,
      default: false,
      required: false,
    },
  },
  computed: {
    ...mapGetters({
      solutions: 'system/getSolutionPhases',
    }),
    innerValue: {
      get() {
        return this.value + 1
      },
      set(value) {
        this.$emit('change', value - 1)
      },
    },
  },
}
</script>

<style lang="less" scoped>
.select-solution-phase {
  width: 250px;
}
</style>
