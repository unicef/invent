<template>
  <div class="TeamList">
    <ul v-show="team.length > 0 || unknown > 0 || unlisted.length > 0">
      <li v-for="p in unlisted" :key="p">
        {{ p }}
      </li>
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
    unlisted() {
      if (this.value) {
        return this.value.filter((p) => p !== p * 1)
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
