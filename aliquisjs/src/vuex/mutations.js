import * as types from './mutation_types'

function lowerCaseLettersExceptFirst (value) {
  return value.replace(/[^\s-]+/g,
    (word) => word.charAt(0) + word.slice(1).toLowerCase())
}

export default {
  [types.UPDATE_SIGN_UP_FIRST_NAME] (state, value) {
    state.signUpFirstName = lowerCaseLettersExceptFirst(value.trim())
  },
  [types.UPDATE_SIGN_UP_SURNAME] (state, value) {
    state.signUpSurname = lowerCaseLettersExceptFirst(value.trim())
  },
  [types.UPDATE_SIGN_UP_DISPLAY_NAME] (state, value) {
    state.signUpDisplayName = value.trim()
  },
  [types.UPDATE_SIGN_UP_EMAIL] (state, value) {
    state.signUpEmail = value.trim()
  },
  [types.UPDATE_SIGN_UP_USERNAME] (state, value) {
    state.signUpUsername = value.trim().replace(/[^\w]/g, '').toLowerCase()
  },
  [types.UPDATE_SIGN_UP_PASSWORD] (state, value) {
    state.signUpPassword = value.trim()
  }
}
