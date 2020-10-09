<template>
  <div class="GoalAreaItem">
    {{ selected }}
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  props: {
    value: {
      type: Number,
      default: null,
    },
  },
  computed: {
    ...mapGetters({
      items: 'projects/getGoalAreas',
    }),
    selected() {
      const found = this.items.find((i) => i.id === this.value)
      return found ? found.name : 'N/A'
    },
  },
}
</script>

<style lang="less">
.GoalAreaItem {
  width: 100%;
}
</style>
