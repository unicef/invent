<template>
  <div class="PlatformList">
    <ul>
      <li
        v-for="p in selected"
        :key="p.id"
      >
        <span>
          {{ p.name }}
        </span>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  components: {
  },
  props: {
    platforms: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    ...mapGetters({
      technologyPlatforms: 'projects/getTechnologyPlatforms'
    }),
    selected () {
      return this.technologyPlatforms.filter(tp => this.platforms.includes(tp.id));
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .PlatformList {
    width: 100%;
  }
</style>
