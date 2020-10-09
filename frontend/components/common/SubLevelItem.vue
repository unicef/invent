<template>
  <div v-if="subLevel" class="SubLevelItem">
    {{ subLevel.name }}
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  props: {
    id: {
      type: [Number, String],
      required: true,
    },
  },
  computed: {
    ...mapGetters({
      getSubLevelDetails: 'countries/getSubLevelDetails',
    }),
    subLevel() {
      return this.getSubLevelDetails(this.id)
    },
  },
}
</script>

<style></style>
