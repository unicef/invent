<template>
  <div class="Toolkit">
    <nuxt-child />
  </div>
</template>

<script>
import { fetchProjectData } from '@/utilities/projects';
export default {
  components: {
  },
  async fetch ({ store, params, error }) {
    store.dispatch('landing/resetSearch');
    try {
      await fetchProjectData(store, params, error);
    } catch (e) {
      return;
    }
    await store.dispatch('projects/loadUserProjects');
    await store.dispatch('toolkit/loadToolkitData');
  }
};
</script>

<style>

</style>
