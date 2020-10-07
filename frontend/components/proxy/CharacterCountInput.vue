<template>
  <div class="CharacterCountInput">
    <el-input v-bind="propsAndAttrs" v-on="listeners" />
    <span v-if="max" :class="['Count', { Error: error }]">
      {{ count }} / {{ max }}
    </span>
  </div>
</template>

<script>
import get from 'lodash/get'

export default {
  name: 'CharacterCountInput',
  props: {
    value: {
      type: null,
      required: true,
    },
    rules: {
      type: Object,
      default: () => ({}),
    },
  },
  computed: {
    propsAndAttrs() {
      return { ...this.$props, ...this.$attrs }
    },
    listeners() {
      return { ...this.$listeners }
    },
    count() {
      if (this.value) {
        return this.value.length
      }
      return 0
    },
    max() {
      return get(this, 'rules.max', null)
    },
    error() {
      return this.count && this.max && this.count > this.max
    },
  },
}
</script>

<style lang="less">
.CharacterCountInput {
  .Count {
    height: 15px;
    line-height: 15px;
    position: absolute;
    top: -15px;
    right: 0;
    font-size: 12px;
  }

  .Error {
    color: #f44336;
  }

  textarea.el-textarea__inner {
    padding-bottom: 15px;
  }
}
</style>
