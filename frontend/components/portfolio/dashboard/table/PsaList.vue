<template>
  <ul class="psa-list">
    <li
      v-for="(item, i) in statements(items)"
      :key="i"
      :class="`${big && 'big'}`"
    >
      <fa class="triangle-icon" :icon="['fas', 'caret-right']" />
      {{ item.name }}
    </li>
  </ul>
</template>

<script>
export default {
  props: {
    items: {
      type: Array,
      required: true,
    },
    problemStatements: {
      type: Array,
      required: true,
    },
    big: {
      type: Boolean,
      required: false,
      default: false,
    },
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
    &.big {
      font-size: 14px;
      margin-bottom: 10px;
      .triangle-icon {
        margin-right: 8px;
        font-size: 16px;
      }
    }
  }
}
</style>
