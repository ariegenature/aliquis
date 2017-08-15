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
  }
}
