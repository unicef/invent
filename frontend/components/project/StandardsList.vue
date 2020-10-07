<template>
  <div class="StandardsList">
    <ul>
      <li v-for="standard in selected" :key="standard.id">
        {{ standard.name }}
      </li>
      <li v-show="selected.length === 0">N/A</li>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  props: {
    value: {
      type: Array,
      default: null,
    },
  },
  computed: {
    ...mapGetters({
      standards: 'projects/getInteroperabilityStandards',
    }),
    selected() {
      return this.standards.filter((hfa) => this.value.includes(hfa.id))
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.StandardsList {
  width: 100%;
}
</style>
