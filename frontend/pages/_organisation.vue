<template>
  <div>
    <nuxt-child />
  </div>
</template>

<script>
// NOTE: This is only a router view wrapper, for common fetches
import { mapGetters } from 'vuex'

export default {
  components: {},
  middleware: ['profile'],
  async fetch({ store, params }) {
    store.dispatch('system/loadUserProfiles')
    await Promise.all([
      store.dispatch('system/loadStaticData'),
      store.dispatch('system/loadDonors'),
      store.dispatch('countries/loadMapData'),
      store.dispatch('landing/search'),
    ])
    if (params.organisation !== '-') {
      await store.dispatch('landing/loadCustomLandingPage', params.organisation)
      await store.dispatch('landing/loadCountryProjectsList')
    } else {
      store.dispatch('landing/clearCustomLandingPage')
    }
    if (store.getters['user/getProfile']) {
      await Promise.all([store.dispatch('system/loadOrganisations')])
    }
  },
  computed: {
    ...mapGetters({
      userProfile: 'user/getProfile',
    }),
  },
  watch: {
    userProfile: {
      immediate: true,
      handler(profile) {},
    },
  },
}
</script>

<style lang="sass"></style>
