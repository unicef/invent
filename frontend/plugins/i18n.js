import Vue from 'vue';
import TranslateWrapper from '../components/TranslateWrapper';

Vue.component('translate', TranslateWrapper);

Vue.mixin({
  methods: {
    $gettext (word, parameters, debug) {
      let translated = this.$t(word, parameters);
      if (debug) {
        console.log(this.$i18n.messages[this.$i18n.locale][word]);
        console.log(this.$te(word));
        console.log(`${word} => ${translated}`, parameters);
      }
      if (!this.$te(word) && parameters) {
        for (let k in parameters) {
          translated = translated.replace(`{${k}}`, parameters[k]);
        }
      }
      return translated;
    }
  }
});

Vue.filter('translate', value => value);

export default function ({ app: { store, i18n } }) {
  // beforeLanguageSwitch called right before setting a new locale
  i18n.beforeLanguageSwitch = (oldLocale, newLocale) => {
  };
  // onLanguageSwitched called right after a new locale has been set
  i18n.onLanguageSwitched = (oldLocale, newLocale) => {
    store.dispatch('system/loadStaticData');
    store.dispatch('projects/loadProjectStructure', true);
  };
};
