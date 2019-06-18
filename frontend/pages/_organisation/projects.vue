<template>
  <div class="ProjectsArea">
    <nuxt-child />
  </div>
</template>

<script>
export default {
  components: {
  },
  async fetch ({ store }) {
    store.dispatch('landing/resetSearch');
    await Promise.all([
      store.dispatch('projects/loadUserProjects'),
      store.dispatch('projects/loadProjectStructure')
    ]);
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .ProjectsArea {
    margin-bottom: 120px;

    .UserProjectsList {
      .limitPageWidth();
      max-width: @cardSizeMedium;
    }
  }
</style>
