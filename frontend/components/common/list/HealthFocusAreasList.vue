<template>
  <div class="HealthFocusAreasList">
    <ul>
      <li v-for="hfa in limited" :key="hfa.id">
        <list-action v-if="actions" @click="$emit('delete', hfa.id)" />
        <span>
          <fa icon="check" size="xs" />
        </span>
        <span>{{ hfa.name }}</span>
      </li>
      <li v-show="excluded > 0">
        <span>
          <fa icon="check" size="xs" />
        </span>
        <span>
          <translate :parameters="{ excluded }">
            ... {excluded} more
          </translate>
        </span>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ListAction from './ListAction'
export default {
  components: {
    ListAction,
  },
  props: {
    value: {
      type: Array,
      default: () => [],
    },
    actions: {
      type: Boolean,
      default: false,
    },
    limit: {
      type: Number,
      default: null,
    },
  },
  computed: {
    ...mapGetters({
      healthFocusAreas: 'projects/getHealthFocusAreas',
    }),
    selected() {
      const hfas = this.healthFocusAreas.reduce(
        (a, c) => [...a, ...c.health_focus_areas],
        []
      )
      return hfas.filter((hfa) => this.value.includes(hfa.id))
    },
    limited() {
      return this.limit ? this.selected.slice(0, this.limit) : this.selected
    },
    excluded() {
      return this.selected.length - this.limited.length
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.HealthFocusAreasList {
  width: 100%;
}
</style>
