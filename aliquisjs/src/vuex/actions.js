import * as types from './mutation_types'

export default {
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
