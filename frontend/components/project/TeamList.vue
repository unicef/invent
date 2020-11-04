<template>
  <div class="TeamList">
    <ul v-show="team.length > 0 || unknown > 0">
      <li v-for="p in team" :key="p.id">
        {{ p.name }}
      </li>
      <li v-show="unknown > 0">
        <translate>+ {{ unknown }} members</translate>
      </li>
    </ul>
    <span v-show="team.length === 0 && unknown === 0">
      <!-- N/A -->
    </span>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  components: {},
  props: {
    value: {
      type: Array,
      default: null,
    },
  },
  computed: {
    ...mapGetters({
      profiles: 'system/getUserProfilesNoFilter',
    }),
    team() {
      if (this.value) {
        return this.profiles.filter((p) => this.value.includes(p.id) && p.name)
      }
      return []
    },
    unknown() {
      return this.profiles.filter(
        (p) => this.value.includes(p.id) && p.name === null
      ).length
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.TeamList {
  width: 100%;
}
</style>
