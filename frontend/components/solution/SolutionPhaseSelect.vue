<template>
  <lazy-el-select
    v-model="innerValue"
    :multiple="false"
    :disabled="disabled"
    :placeholder="$gettext('Phase') | translate"
    filterable
    class="select-solution-phase"
  >
    <el-option v-for="solution in solutionList" :key="solution.id" :label="solution.name" :value="solution.id" />
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
      type: [Number, Array],
      default: null,
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
        return this.value
      },
      set(value) {
        this.$emit('change', value)
      },
    },
    solutionList() {
      return this.solutions ? this.solutions : []
    },
  },
}
</script>

<style lang="less" scoped>
.select-solution-phase {
  width: 250px;
}
</style>
