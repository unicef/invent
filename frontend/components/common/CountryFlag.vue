<template>
  <img :class="['CountryFlag', `${size}`]" :src="countryFlagUrl" loading="lazy" />
</template>

<script>
export default {
  props: {
    code: {
      type: String,
      default: null,
    },
    size: {
      type: String,
      default: '',
      validator: (value) => {
        return ['', 'small', 'tiny'].includes(value)
      },
    },
  },
  computed: {
    countryFlagUrl() {
      if (this.code) {
        return `/static/flags/${this.code.toLowerCase()}.png`
      }
      return null
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.CountryFlag {
  &.small {
    height: 16px;
  }
  &.tiny {
    height: 12px;
  }
}
</style>
