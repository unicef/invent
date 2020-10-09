<template>
  <el-select v-bind="propsAndAttrs" v-on="listeners">
    <template v-if="open">
      <slot />
    </template>
  </el-select>
</template>

<script>
export default {
  name: 'LazyElSelect',
  props: {
    value: {
      type: null,
      required: true,
    },
  },
  data() {
    return {
      open: false,
    }
  },
  computed: {
    propsAndAttrs() {
      return { ...this.$props, ...this.$attrs }
    },
    listeners() {
      return { ...this.$listeners, 'visible-change': this.onVisibleChange }
    },
  },
  watch: {
    value: {
      immediate: false,
      handler(value) {
        if (!this.open && value) {
          this.open = true
        }
      },
    },
  },
  mounted() {
    if (this.value) {
      window.requestAnimationFrame(() => {
        this.open = true
      })
    }
  },
  methods: {
    onVisibleChange(value) {
      if (value && !this.open) {
        this.open = true
      }
    },
  },
}
</script>

<style></style>
