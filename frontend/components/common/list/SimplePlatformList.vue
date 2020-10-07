<template>
  <div class="SimplePlatformList">
    <ul>
      <li v-for="p in selected" :key="p.id">
        <list-action v-if="actions" @click="$emit('delete', p.id)" />
        <span>{{ p.name }}</span>
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
      default: null,
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
      platforms: 'projects/getTechnologyPlatforms',
    }),
    selected() {
      const result = this.platforms.filter((p) => this.value.includes(p.id))
      return this.limit ? result.slice(0, this.limit) : result
    },
  },
}
</script>

<style lang="less">
.SimplePlatformList {
  width: 100%;
}
</style>
