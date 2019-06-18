<template>
  <div class="TeamList">
    <ul v-show="team.length > 0">
      <li
        v-for="p in team"
        :key="p.id"
      >
        {{ p.name }}
      </li>
    </ul>
    <span v-show="team.length === 0">
      <translate>N/A</translate>
    </span>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  components: {
  },
  props: {
    value: {
      type: Array,
      default: null
    }
  },
  computed: {
    ...mapGetters({
      profiles: 'system/getUserProfiles'
    }),
    team () {
      if (this.value) {
        return this.profiles.filter(p => this.value.includes(p.id));
      }
      return [];
    }
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .TeamList {
    width: 100%;
  }
</style>
