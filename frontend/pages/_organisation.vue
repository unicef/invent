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
    await Promise.all([
      store.dispatch('system/loadStaticData'),
      store.dispatch('system/loadDonors'),
      store.dispatch('countries/loadMapData'),
      store.dispatch('landing/search'),
    ])
    if (params.organisation !== '-') {
      await store.dispatch('landing/loadCustomLandingPage', params.organisation)
    } else {
      store.dispatch('landing/clearCustomLandingPage')
    }
    if (store.getters['user/getProfile']) {
      await Promise.all([
        store.dispatch('projects/loadUserProjects'),
        store.dispatch('system/loadOrganisations'),
        store.dispatch('system/loadUserProfiles'),
      ])
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
      handler(profile) {
        if (this.$sentry) {
          this.$sentry.configureScope((scope) => {
            scope.setUser(profile)
          })
        }
      },
    },
  },
}
</script>

<style lang="sass"></style>
