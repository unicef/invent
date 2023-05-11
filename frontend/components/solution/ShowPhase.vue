<template>
  <p>{{ getPhaseName(phaseId) }}</p>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  props: {
    phaseId: {
      type: Number,
    },
  },
  computed: {
    ...mapGetters({ phases: 'system/getSolutionPhases' }),
  },
  methods: {
    getPhaseName(id) {
      return this.phases.find((phase) => phase.id === id).name
    },
  },
}
</script>

<style></style>
