<template>
  <div class="HealthFocusAreasList">
    <ul>
      <li v-for="hfa in selected" :key="hfa.id">
        <list-action v-if="actions" @click="$emit('delete', hfa.id)" />
        <span v-if="showCheck">
          <fa icon="check" size="xs" />
        </span>
        <span> {{ hfa.name }} </span>
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
    valueIsChild: {
      type: Boolean,
      default: false,
    },
    showCheck: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapGetters({
      healthFocusAreas: 'projects/getHealthFocusAreas',
    }),
    selected() {
      let result = []
      if (!this.valueIsChild) {
        result = this.healthFocusAreas.filter((h) => this.value.includes(h.id))
      } else {
        result = this.healthFocusAreas.filter((hfa) =>
          hfa.health_focus_areas.some((hfaInner) =>
            this.value.includes(hfaInner.id)
          )
        )
      }
      return this.limit ? result.slice(0, this.limit) : result
    },
  },
}
</script>

<style lang="less">
.HealthFocusAreasList {
  width: 100%;
}
.HealthFocusAreasSelectorDropdown {
}
</style>
