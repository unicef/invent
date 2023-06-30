import Vue from 'vue'
import TranslateWrapper from '../components/TranslateWrapper'

Vue.component('Translate', TranslateWrapper)

Vue.mixin({
  methods: {
    $gettext(word, parameters, debug) {
      if (!word) {
        return ''
      }
      const trimmedWord = word
        .replace(/\s+\n/g, '\n')
        .replace(/\n\s+/g, '\n')
        .replace(/\t/g, ' ')
        .replace(/\n/g, ' ')
        .replace(/ +/g, ' ')
      let translated = this.$t(trimmedWord, parameters)

      if (debug) {
        console.log(this.$i18n.messages[this.$i18n.locale][trimmedWord])
        console.log(this.$te(trimmedWord))
        console.log(`${trimmedWord} => ${translated}`, parameters)
      }
      if (!this.$te(trimmedWord) && parameters) {
        for (const k in parameters) {
          translated = translated.replace(`{${k}}`, parameters[k])
        }
      }
      return translated
    },
  },
})

Vue.filter('translate', (value) => value)

export default function ({ app: { store, i18n } }) {
  // beforeLanguageSwitch called right before setting a new locale
  i18n.beforeLanguageSwitch = (oldLocale, newLocale) => {}
  // onLanguageSwitched called right after a new locale has been set
  i18n.onLanguageSwitched = (oldLocale, newLocale) => {
    store.dispatch('system/loadStaticData')
    store.dispatch('projects/loadProjectStructure', true)
  }
}
