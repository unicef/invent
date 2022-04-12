<template>
  <span v-if="dhi" class="DhiItem">
    {{ dhi.name }}
  </span>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  props: {
    id: {
      type: Number,
      required: true,
    },
  },
  computed: {
    ...mapGetters({
      getDigitalHealthInterventionDetails: 'projects/getDigitalHealthInterventionDetails',
    }),
    dhi() {
      return this.getDigitalHealthInterventionDetails(this.id)
    },
  },
}
</script>

<style lang="less">
.DhiItem {
  display: inline;
}
</style>
