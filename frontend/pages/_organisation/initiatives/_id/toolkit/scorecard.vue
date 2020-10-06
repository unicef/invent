<template>
  <div class="angularjs">
    <div id="toolkitjs" />
  </div>
</template>

<script>

export default {
  components: {
  },
  mounted () {
    const mapsToolkitFactory = require('../../../../../angular/MapsToolkit/mapsToolkitFactory');
    mapsToolkitFactory.factory();
  }
};
</script>

<style>

</style>
