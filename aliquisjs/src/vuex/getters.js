export default {
  getSignUpFirstName: state => state.signUpFirstName,
  getSignUpSurname: state => state.signUpSurname,
  getSignUpDisplayName: state => {
    if (state.signUpDisplayName) {
      return state.signUpDisplayName
    }
    var firstName = state.signUpFirstName
    var surname = state.signUpSurname
    if (firstName && surname) {
      return `${firstName} ${surname}`
    }
    if (firstName) {
      return `${firstName}`
    }
    if (surname) {
      return `${surname}`
    }
    return ''
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
  validateSignUpData: (state, getters) => (Boolean(
    state.signUpFirstName &&
    state.signUpSurname &&
    getters.getSignUpDisplayName &&
    state.signUpEmail.match(state.emailRegExp) &&
    getters.getSignUpUsername.match(state.usernameRegExp) &&
    state.signUpPassword.length >= 6
  ))
}
