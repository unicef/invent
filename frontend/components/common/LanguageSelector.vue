<template>
  <div class="LanguageSelector">
    <div
      v-for="locale in localesButArabic"
      :key="locale.code"
      class="LanguageLink"
    >
      <nuxt-link :to="switchLocalePath(locale.code)" class="HeaderBtn">
        {{ locale.name }}
      </nuxt-link>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    localesButArabic() {
      return this.$i18n.locales.filter((la) => la.code !== 'ar')
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.LanguageSelector {
  .clearfix();

  .LanguageLink {
    float: left;
  }
}
</style>
