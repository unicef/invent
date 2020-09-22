<template>
  <span class="Element">
    {{ selected.name }}
  </span>
</template>

<script>
export default {
  components: {
  },
  props: {
    value: {
      type: Number,
      required: true
    },
    source: {
      type: String,
      default: 'getTechnologyPlatforms'
    }
  },
  computed: {
    selected () {
      const value = this.value;
      const list = this.$store.getters[`projects/${this.source}`];
      return list.find(e => e.id === value);
    }
  }
};
</script>

<style lang="less">
</style>
