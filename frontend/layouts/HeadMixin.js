export default {
  head () {
    const i18nSeo = this.$nuxtI18nSeo();
    return {
      htmlAttrs: {
        ...i18nSeo.htmlAttrs,
        dir: this.$_headMixin_lngDirection
      },
      meta: [
        ...i18nSeo.meta
      ],
      link: [
        ...i18nSeo.link
      ]
    };
  },
  computed: {
    $_headMixin_lngDirection () {
      if (this.$i18n.locale === 'ar') {
        return 'rtl';
      }
      return 'ltr';
    }
  }
};
