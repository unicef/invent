<template>
  <span class="PageCounter">
    <translate :parameters="{ min, max, total }">
      {min}-{max} of {total}
    </translate>
  </span>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters({
      total: 'dashboard/getTotal',
      pageSize: 'dashboard/getPageSize',
      currentPage: 'dashboard/getCurrentPage',
    }),
    min() {
      return 1 + this.pageSize * (this.currentPage - 1)
    },
    max() {
      const max = this.pageSize * this.currentPage
      return max < this.total ? max : this.total
    },
  },
}
</script>

<style></style>
