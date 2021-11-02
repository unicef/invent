import Vue from 'vue'
import { format } from 'date-fns'

Vue.filter('simpleDateFormat', (value) => {
  return value ? format(value, 'DD/MM/YYYY') : ''
})

export default ({store}) => {
  Vue.filter('formatNumber', (value) => {
    return new Intl.NumberFormat(store.$i18n.localeProperties.iso).format(value)
  })
}