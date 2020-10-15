<template>
  <span class="PageCounter">
    <translate :parameters="{ min, max, total }">
      {min}-{max} of {total}
    </translate>
  </span>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState({
      total: (state) => state.portfolio.total,
      pageSize: (state) => state.search.filter.page_size,
      page: (state) => state.search.filter.page,
    }),
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
