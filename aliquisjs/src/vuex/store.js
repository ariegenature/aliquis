import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'

Vue.use(Vuex)

const state = {
  signUpFirstName: '',
  signUpSurname: '',
  signUpDisplayName: '',
  signUpEmail: '',
  signUpUsername: '',
  signUpPassword: '',
  emailRegExp: /^([a-zA-Z0-9.+-]+@[a-zA-Z\d-]+(\.[a-zA-Z\d-]+)+)$/,
  usernameRegExp: /^[a-z][a-z0-9_.]+$/
}

export default new Vuex.Store({
  state,
  getters
})
