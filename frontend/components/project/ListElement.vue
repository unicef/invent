<template>
  <span class="Element">
    {{ selected ? selected.name : '' }}
  </span>
</template>

<script>
export default {
  components: {},
  props: {
    value: {
      type: [Number, Object],
      default: null,
    },
    source: {
      type: String,
      default: 'getTechnologyPlatforms',
    },
    root: {
      type: String,
      default: 'projects',
    },
  },
  computed: {
    selected() {
      const value = this.value
      const list = this.$store.getters[`${this.root}/${this.source}`]
      return list ? list.find((e) => e.id === value) : {}
    },
  },
}
</script>

<style lang="less"></style>
