<template>
  <div class="ProfilePage">
    <edit-profile />
  </div>
</template>

<script>
import EditProfile from '../../components/EditProfile.vue';

export default {
  components: {
    EditProfile
  },
  watchQuery: ['missingProfile'],
  async fetch ({ store, query, redirect }) {
    if (query && query.missingProfile) {
      store.dispatch('layout/setShowEmptyProfileWarning', true);
      redirect({ ...this.$route, query: undefined });
      return;
    }
    await store.dispatch('system/loadDonors');
  }
};
</script>

<style lang="less">
</style>
