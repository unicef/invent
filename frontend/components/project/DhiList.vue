<template>
  <div class="DHIList">
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
import { mapGetters } from 'vuex'

export default {
  components: {},
  props: {
    values: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    ...mapGetters({
      dhis: 'projects/getDigitalHealthInterventions',
    }),
    flattened() {
      return this.dhis.reduce((a, c) => {
        const inner = c.subGroups.reduce((innerA, innerC) => {
          return innerA.concat(innerC.strategies)
        }, [])
        return a.concat(inner)
      }, [])
    },
    selected() {
      return this.flattened.filter((tp) => this.values.includes(tp.id))
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.DHIList {
  width: 100%;
}
</style>
