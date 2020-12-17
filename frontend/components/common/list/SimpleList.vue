<template>
  <div v-if="items">
    <p v-for="item in items" :key="item" :style="{ marginBottom: '6px' }">
      {{ item }}
    </p>
  </div>
</template>

<script>
export default {
  props: {
    items: {
      // type: [Array, String],
      required: true,
      validator: (prop) => Array.isArray(prop) || prop === null,
    },
  },
}
</script>
