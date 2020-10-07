<template>
  <div class="ProfilePage">
    <edit-profile />
  </div>
</template>

<script>
import EditProfile from '../../components/EditProfile.vue'

export default {
  components: {
    EditProfile,
  },
  async fetch({ store, query, redirect }) {
    if (query && query.missingProfile) {
      store.dispatch('layout/setShowEmptyProfileWarning', true)
      redirect({ ...this.$route, query: undefined })
      return
    }
    await store.dispatch('system/loadDonors')
  },
  watchQuery: ['missingProfile'],
}
</script>

<style lang="less"></style>
