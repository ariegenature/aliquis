import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import mutations from './mutations'
import actions from './actions'

Vue.use(Vuex)

const state = {
  firstName: '',
  surname: '',
  displayName: '',
  email: '',
  username: '',
  description: '',
  isActive: false,
  newEmail: '',
  signUpFirstName: '',
  signUpSurname: '',
  signUpDisplayName: '',
  signUpEmail: '',
  signUpUsername: '',
  signUpPassword: '',
  statusMessage: '',
  statusMessageClass: '',
  isLoading: false,
  emailRegExp: /^([a-zA-Z0-9.+-]+@[a-zA-Z\d-]+(\.[a-zA-Z\d-]+)+)$/,
  usernameRegExp: /^[a-z][a-z0-9_.]+$/
}

export default new Vuex.Store({
  state,
  getters,
  mutations,
  actions
})
