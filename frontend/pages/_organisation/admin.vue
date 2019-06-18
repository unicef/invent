<template>
  <div>
    <nuxt-child />
  </div>
</template>

<script>
// NOTE: This is only a router view wrapper, for common fetches
import { mapGetters } from 'vuex';

export default {
  components: {
  },
  middleware: ['isLoggedIn'],
  async fetch ({ store }) {
    store.dispatch('landing/resetSearch');
  },
  computed: {
    ...mapGetters({
    })
  }
};
</script>

<style lang="less">
</style>
