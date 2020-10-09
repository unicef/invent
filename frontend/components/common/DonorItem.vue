<template>
  <div v-if="donor" class="DonorItem">
    {{ donor.name }}
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
      getDonorDetails: 'system/getDonorDetails',
    }),
    donor() {
      if (this.id) {
        const id = parseInt(this.id, 10)
        return this.getDonorDetails(id)
      }
      return null
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';
</style>
