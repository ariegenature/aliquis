import api from '../api'
import * as types from './mutation_types'

export default {
  fetchAndInitUser ({ commit }, value) {
    commit(types.SET_PAGE_LOADING)
    api.fetchUser(value).then(response => {
      commit(types.INIT_USER, response.data)
    }, response => {
      commit(types.CLEAR_USER)
    })
    api.fetchGrants(value).then(response => {
      commit(types.UPDATE_GRANTS, response.data)
    }, response => {
      commit(types.CLEAR_GRANTS)
    })
    commit(types.SET_PAGE_NOT_LOADING)
  },
  confirmUser ({ commit }, value) {
    commit(types.SET_PAGE_LOADING)
    api.confirmUser(value).then(response => {
      commit(types.UPDATE_STATUS_MESSAGE, response.data)
      commit(types.SET_PAGE_NOT_LOADING)
    }, response => {
      commit(types.UPDATE_STATUS_MESSAGE, response.data)
      commit(types.SET_PAGE_NOT_LOADING)
    })
  },
  reactivateUser ({ commit }, value) {
    commit(types.SET_PAGE_LOADING)
    api.reactivateUser(value).then(response => {
      commit(types.UPDATE_STATUS_MESSAGE, response.data)
      commit(types.SET_PAGE_NOT_LOADING)
    }, response => {
      commit(types.UPDATE_STATUS_MESSAGE, response.data)
      commit(types.SET_PAGE_NOT_LOADING)
    })
  },
  [types.UPDATE_FIRST_NAME] ({ commit }, value) {
    commit(types.UPDATE_FIRST_NAME, value)
  },
  [types.UPDATE_SURNAME] ({ commit }, value) {
    commit(types.UPDATE_SURNAME, value)
  },
  [types.UPDATE_DISPLAY_NAME] ({ commit }, value) {
    commit(types.UPDATE_DISPLAY_NAME, value)
  },
  [types.UPDATE_EMAIL] ({ commit }, value) {
    commit(types.UPDATE_EMAIL, value)
  },
  [types.UPDATE_DESCRIPTION] ({ commit }, value) {
    commit(types.UPDATE_DESCRIPTION, value)
  },
  [types.UPDATE_NEW_EMAIL] ({ commit }, value) {
    commit(types.UPDATE_NEW_EMAIL, value)
  },
  [types.CLEAR_NEW_EMAIL] ({ commit }) {
    commit(types.CLEAR_NEW_EMAIL)
  },
  [types.UPDATE_SIGN_UP_FIRST_NAME] ({ commit }, value) {
    commit(types.UPDATE_SIGN_UP_FIRST_NAME, value)
  },
  [types.UPDATE_SIGN_UP_SURNAME] ({ commit }, value) {
    commit(types.UPDATE_SIGN_UP_SURNAME, value)
  },
  [types.UPDATE_SIGN_UP_DISPLAY_NAME] ({ commit }, value) {
    commit(types.UPDATE_SIGN_UP_DISPLAY_NAME, value)
  },
  [types.UPDATE_SIGN_UP_EMAIL] ({ commit }, value) {
    commit(types.UPDATE_SIGN_UP_EMAIL, value)
  },
  [types.UPDATE_SIGN_UP_USERNAME] ({ commit }, value) {
    commit(types.UPDATE_SIGN_UP_USERNAME, value)
  },
  [types.UPDATE_SIGN_UP_PASSWORD] ({ commit }, value) {
    commit(types.UPDATE_SIGN_UP_PASSWORD, value)
  },
  [types.CLEAR_SIGN_UP_DATA] ({ commit }) {
    commit(types.CLEAR_SIGN_UP_DATA)
  },
  [types.UPDATE_STATUS_MESSAGE] ({ commit }, value) {
    commit(types.UPDATE_STATUS_MESSAGE, value)
  },
  [types.CLEAR_STATUS_MESSAGE] ({ commit }) {
    commit(types.CLEAR_STATUS_MESSAGE)
  },
  [types.SET_PAGE_LOADING] ({ commit }) {
    commit(types.SET_PAGE_LOADING)
  },
  [types.SET_PAGE_NOT_LOADING] ({ commit }) {
    commit(types.SET_PAGE_NOT_LOADING)
  }
}
