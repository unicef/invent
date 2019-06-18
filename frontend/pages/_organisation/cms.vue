<template>
  <div class="angularjs">
    <div id="cmsjs" />
  </div>
</template>

<script>

export default {
  components: {
  },

  middleware: ['isLoggedIn'],
  fetch ({ store }) {
    store.dispatch('landing/resetSearch');
  },
  mounted () {
    const cmsFactory = require('../../angular/Cms/cmsFactory');
    cmsFactory.cmsFactory();
  }
};
</script>

<style>

</style>
