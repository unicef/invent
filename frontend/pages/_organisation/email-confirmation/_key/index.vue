<template>
  <div class="">
    <dha-verify />
  </div>
</template>

<script>
import DhaVerify from '../../../../components/DhaVerify';

export default {

  components: { DhaVerify },

  async fetch ({ params, store }) {
    await store.dispatch('user/verifyEmail', params.key);
  }
};
</script>

<style lang="less">
</style>
