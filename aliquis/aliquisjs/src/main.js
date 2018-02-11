// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import App from './App'
import Buefy from 'buefy'
import VeeValidate, { Validator } from 'vee-validate'
import Vue from 'vue'
import VueResource from 'vue-resource'
import fr from 'vee-validate/dist/locale/fr'
import router from './router'
import 'buefy/lib/buefy.css'

var locale = navigator.languages !== undefined ? navigator.languages[0] : navigator.language
locale = locale.substring(0, 2)

Vue.config.productionTip = false

Vue.use(Buefy, {
  defaultIconPack: 'fa'
})

Validator.localize('fr', fr)
Vue.use(VeeValidate, {
  events: '',
  locale: locale
})
Vue.use(VueResource)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
