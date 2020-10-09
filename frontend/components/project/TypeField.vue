<template>
  <div class="TypeField">
    {{ selected }}
  </div>
</template>

<script>
export default {
  props: {
    list: {
      type: Array,
      default: () => [],
    },
    value: {
      type: Number,
      default: null,
    },
  },
  computed: {
    selected() {
      return this.list[this.value]
    },
  },
}
</script>

<style></style>
