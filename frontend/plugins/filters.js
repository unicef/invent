import Vue from 'vue'
import { format } from 'date-fns'

Vue.filter('simpleDateFormat', (value) => {
  return value ? format(value, 'DD/MM/YYYY') : ''
})

Vue.filter('formatNumber', (value) => {
  return new Intl.NumberFormat().format(value)
})
