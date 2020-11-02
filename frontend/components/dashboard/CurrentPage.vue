<template>
  <span class="PageCounter">
    <translate :parameters="{ min, max, total }">
      {min}-{max} of {total}
    </translate>
  </span>
</template>

<script>
export default {
  props: {
    total: {
      type: Number,
      required: true,
    },
    pageSize: {
      type: Number,
      required: true,
    },
    page: {
      type: Number,
      required: true,
    },
  },
  computed: {
    min() {
      return 1 + this.pageSize * (this.page - 1)
    },
    max() {
      const max = this.pageSize * this.page
      return max < this.total ? max : this.total
    },
  },
}
</script>

<style></style>
