<template>
  <div class="AdminImportPage">
    <nuxt-child />
  </div>
</template>

<script>
export default {
  components: {},
  middleware: ['importRestriction'],
}
</script>

<style></style>
