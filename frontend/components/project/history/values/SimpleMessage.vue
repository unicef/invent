<template>
  <span>{{ changes.message }}</span>
</template>

<script>
export default {
  props: {
    changes: {
      type: Object,
      required: true,
    },
  },
}
</script>
