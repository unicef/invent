import Vue from 'vue';
Vue.config.productionTip = false;
Vue.config.performance = !process.env.NODE_ENV || !process.env.NODE_ENV.production;
