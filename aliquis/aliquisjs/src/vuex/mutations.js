import * as types from './mutation_types'

function lowerCaseLettersExceptFirst (value) {
  return value.replace(/[^\s-]+/g,
    (word) => word.charAt(0) + word.slice(1).toLowerCase())
}

const classes = ['', 'is-primary', 'is-info', 'is-success', 'is-warning', 'is-danger']

export default {
  [types.INIT_USER] (state, data) {
    var firstName = lowerCaseLettersExceptFirst(data['first_name'])
    var surname = lowerCaseLettersExceptFirst(data['surname'])
    state.firstName = firstName
    state.surname = surname
    var displayName = data['display_name']
    state.displayName = displayName === `${firstName} ${surname}` ? '' : displayName
    state.email = data['email']
    state.username = data['username']
    state.isActive = data['is_active']
  },
  [types.CLEAR_USER] (state) {
    state.firstName = ''
    state.surname = ''
    state.displayName = ''
    state.email = ''
    state.username = ''
  },
  [types.UPDATE_FIRST_NAME] (state, value) {
    state.firstName = lowerCaseLettersExceptFirst(value.trim())
  },
  [types.UPDATE_SURNAME] (state, value) {
    state.surname = lowerCaseLettersExceptFirst(value.trim())
  },
  [types.UPDATE_DISPLAY_NAME] (state, value) {
    state.displayName = value.trim()
  },
  [types.UPDATE_EMAIL] (state, value) {
    state.email = value.trim()
  },
  [types.UPDATE_NEW_EMAIL] (state, value) {
    state.newEmail = value.trim()
  },
  [types.CLEAR_NEW_EMAIL] (state) {
    state.newEmail = ''
  },
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
  },
  [types.CLEAR_SIGN_UP_DATA] (state) {
    state.signUpFirstName = ''
    state.signUpSurname = ''
    state.signUpDisplayName = ''
    state.signUpEmail = ''
    state.signUpUsername = ''
    state.signUpPassword = ''
  },
  [types.UPDATE_STATUS_MESSAGE] (state, value) {
    state.statusMessage = value.msg.trim()
    if (classes.indexOf(value.cls.trim()) >= 0) {
      state.statusMessageClass = value.cls.trim()
    }
  },
  [types.CLEAR_STATUS_MESSAGE] (state) {
    state.statusMessage = ''
    state.statusMessageClass = ''
  },
  [types.SET_PAGE_LOADING] (state) {
    state.isLoading = true
  },
  [types.SET_PAGE_NOT_LOADING] (state) {
    state.isLoading = false
  }
}
