function displayNameValue (displayName, firstName, surname) {
  if (displayName) {
    return displayName
  }
  if (firstName && surname) {
    return `${firstName} ${surname}`
  }
  if (firstName) {
    return firstName
  }
  if (surname) {
    return surname
  }
  return ''
}

export default {
  getFirstName: state => state.firstName,
  getSurname: state => state.surname,
  getDisplayName: state => {
    return displayNameValue(state.displayName, state.firstName, state.surname)
  },
  getEmail: state => state.email,
  getUsername: state => state.username,
  getDescription: state => state.description,
  getIsActive: state => state.isActive,
  getNewEmail: state => state.newEmail,
  getSignUpFirstName: state => state.signUpFirstName,
  getSignUpSurname: state => state.signUpSurname,
  getSignUpDisplayName: state => {
    return displayNameValue(state.signUpDisplayName, state.signUpFirstName, state.signUpSurname)
  },
  getSignUpEmail: state => state.signUpEmail,
  getSignUpUsername: state => {
    var username = ''
    if (state.signUpUsername) {
      return state.signUpUsername.replace(/[^\w]/g, '').toLowerCase()
    }
    var firstName = state.signUpFirstName
    var surname = state.signUpSurname
    if (firstName && surname) {
      username = firstName.charAt(0) + surname
    } else if (firstName) {
      username = firstName
    } else if (surname) {
      username = surname
    }
    return username.replace(/[^\w]/g, '').toLowerCase()
  },
  getSignUpPassword: state => state.signUpPassword,
  getStatusMessage: state => state.statusMessage,
  getStatusMessageClass: state => state.statusMessageClass,
  getIsLoading: state => state.isLoading,
  getEmailRegExp: state => state.emailRegExp,
  getUsernameRegExp: state => state.usernameRegExp,
  validateUserData: (state, getters) => (Boolean(
    state.firstName &&
    state.surname &&
    getters.getDisplayName &&
    state.email.match(state.emailRegExp)
  )),
  validateSignUpData: (state, getters) => (Boolean(
    state.signUpFirstName &&
    state.signUpSurname &&
    getters.getSignUpDisplayName &&
    state.signUpEmail.match(state.emailRegExp) &&
    getters.getSignUpUsername.match(state.usernameRegExp) &&
    state.signUpPassword.length >= 6
  )),
  getGrants: state => state.grants
}
