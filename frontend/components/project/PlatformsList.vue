<template>
  <div class="PlatformList">
    <ul>
      <li v-for="p in selected" :key="p.id">
        <span>
          {{ p.name }}
        </span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  components: {},
  props: {
    platforms: {
      type: Array,
      default: () => [],
    },
    source: {
      type: String,
      default: 'getTechnologyPlatforms',
    },
  },
  computed: {
    selected() {
      const list = this.$store.getters[`projects/${this.source}`]
      return list && this.platforms
        ? list.filter((tp) => this.platforms.includes(tp.id))
        : []
    },
  },
}
</script>

<style lang="less">
//@import "~assets/style/variables.less";
//@import "~assets/style/mixins.less";

.PlatformList {
  width: 100%;
}
</style>
