<template>
  <img
    :class="['CountryFlag', {small}]"
    :src="countryFlagUrl"
  >
</template>

<script>
export default {
  props: {
    code: {
      type: String,
      default: null
    },
    small: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    countryFlagUrl () {
      if (this.code) {
        return `/static/flags/${this.code.toLowerCase()}.png`;
      }
      return null;
    }
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .CountryFlag {
    &.small {
      height: 16px;
      width: 24px;
    }
  }
</style>
