<template>
  <donor-admin />
</template>

<script>
import DonorAdmin from '../../../components/admin/DonorAdmin'

export default {
  name: 'Donor',

  components: {
    DonorAdmin,
  },

  async fetch({ store }) {
    await Promise.all([
      store.dispatch('system/loadUserProfiles'),
      store.dispatch('system/loadDonors'),
    ])
    store.dispatch('admin/questions/setQuestionnaireType', 'donor')
    await store.dispatch('admin/donor/fetchData')
  },
}
</script>
