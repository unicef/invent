<template>
  <div class="SignupPage">
    <signup-component :reset="$route.params.key" />
  </div>
</template>

<script>
import SignupComponent from '~/components/SignupComponent';

export default {
  components: {
    SignupComponent
  }
};
</script>

<style lang="less">
</style>
