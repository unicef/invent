<template>
  <country-admin />
</template>

<script>
import CountryAdmin from '../../../components/admin/CountryAdmin';
export default {

  components: { CountryAdmin },

  async fetch ({ store }) {
    await Promise.all([
      store.dispatch('system/loadUserProfiles')
    ]);
    store.dispatch('admin/questions/setQuestionnaireType', 'country');
    await store.dispatch('admin/country/fetchData');
    await store.dispatch('admin/map/loadGeoJSON');
  }
};
</script>
