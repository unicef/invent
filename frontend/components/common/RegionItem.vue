<template>
  <div v-if="region" class="RegionItem">
    {{ region.name }}
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  components: {},
  props: {
    id: {
      type: [String, Number],
      default: null,
    },
  },
  computed: {
    ...mapGetters({
      getRegionDetails: 'system/getRegionDetails',
    }),
    region() {
      const id = parseInt(this.id, 10)
      return this.getRegionDetails(id)
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';
</style>
