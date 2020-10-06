<template>
  <ul class="psa-list">
    <li v-for="(item, i) in statements(items)" :key="i">
      <fa class="triangle-icon" :icon="['fas', 'caret-right']" />
      {{ item.name }}
    </li>
  </ul>
</template>

<script>
import { mapState } from 'vuex'

export default {
  props: {
    items: {
      type: Array,
      required: true,
    },
  },
  computed: {
    ...mapState({
      problemStatements: (state) => state.portfolio.problemStatements,
    }),
  },
  methods: {
    statements(arr) {
      return this.problemStatements.filter((i) => arr.includes(i.id))
    },
  },
}
</script>

<style lang="less" scoped>
.psa-list {
  margin: 0;
  padding: 0;
  list-style: none;
  li {
    font-size: 12px;
    margin-bottom: 4px;
    .triangle-icon {
      color: #a8a8a9;
      margin-right: 5px;
    }
  }
}
</style>
