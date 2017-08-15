import mutations from '../../../../src/vuex/mutations'
import * as types from '../../../../src/vuex/mutation_types'

describe('mutations', () => {
  var state

  beforeEach(() => {
    state = {
      signUpFirstName: 'John',
      signUpSurname: 'Doé',
      signUpDisplayName: '',
      signUpEmail: 'john.doe@example.org',
      signUpUsername: '',
      signUpPassword: 'jdoe1234',
      emailRegExp: /^([a-zA-Z0-9.+-]+@[a-zA-Z\d-]+(\.[a-zA-Z\d-]+)+$)/,
      usernameRegExp: /^[a-z][a-z0-9_.]+$/
    }
  })

  describe(types.UPDATE_SIGN_UP_FIRST_NAME, () => {
    it('should update first name used to sign up', () => {
      mutations[types.UPDATE_SIGN_UP_FIRST_NAME](state, '  JOHNNY   ')
      expect(state.signUpFirstName).to.eql('Johnny')
    })
  })

  describe(types.UPDATE_SIGN_UP_FIRST_NAME + 'Empty', () => {
    it('should update first name used to sign up with empty value', () => {
      mutations[types.UPDATE_SIGN_UP_FIRST_NAME](state, '  ')
      expect(state.signUpFirstName).to.eql('')
    })
  })

  describe(types.UPDATE_SIGN_UP_SURNAME, () => {
    it('should update surname used to sign up', () => {
      mutations[types.UPDATE_SIGN_UP_SURNAME](state, '  DOÉ ')
      expect(state.signUpSurname).to.eql('Doé')
    })
  })

  describe(types.UPDATE_SIGN_UP_SURNAME + 'Empty', () => {
    it('should update surname used to sign up with empty value', () => {
      mutations[types.UPDATE_SIGN_UP_SURNAME](state, '  ')
      expect(state.signUpSurname).to.eql('')
    })
  })

  describe(types.UPDATE_SIGN_UP_DISPLAY_NAME, () => {
    it('should update display name used to sign up', () => {
      mutations[types.UPDATE_SIGN_UP_DISPLAY_NAME](state, '  J. DOÉ ')
      expect(state.signUpDisplayName).to.eql('J. DOÉ')
    })
  })

  describe(types.UPDATE_SIGN_UP_DISPLAY_NAME + 'Empty', () => {
    it('should update display name used to sign up with empty value', () => {
      mutations[types.UPDATE_SIGN_UP_DISPLAY_NAME](state, '  ')
      expect(state.signUpDisplayName).to.eql('')
    })
  })

  describe(types.UPDATE_SIGN_UP_EMAIL, () => {
    it('should update email used to sign up', () => {
      mutations[types.UPDATE_SIGN_UP_EMAIL](state, '   john  ')
      expect(state.signUpEmail).to.eql('john')
    })
  })

  describe(types.UPDATE_SIGN_UP_EMAIL + 'Empty', () => {
    it('should update email used to sign up with empty value', () => {
      mutations[types.UPDATE_SIGN_UP_EMAIL](state, '   ')
      expect(state.signUpEmail).to.eql('')
    })
  })

  describe(types.UPDATE_SIGN_UP_USERNAME, () => {
    it('should update username used to sign up', () => {
      mutations[types.UPDATE_SIGN_UP_USERNAME](state, '  J-Doé  ')
      expect(state.signUpUsername).to.eql('jdo')
    })
  })

  describe(types.UPDATE_SIGN_UP_USERNAME + 'Empty', () => {
    it('should update username used to sign up with empty value', () => {
      mutations[types.UPDATE_SIGN_UP_USERNAME](state, '  ')
      expect(state.signUpUsername).to.eql('')
    })
  })

  describe(types.UPDATE_SIGN_UP_PASSWORD, () => {
    it('should update password used to sign up', () => {
      mutations[types.UPDATE_SIGN_UP_PASSWORD](state, '   jdoe1  ')
      expect(state.signUpPassword).to.eql('jdoe1')
    })
  })

  describe(types.UPDATE_SIGN_UP_PASSWORD + 'Empty', () => {
    it('should update password used to sign up with empty value', () => {
      mutations[types.UPDATE_SIGN_UP_PASSWORD](state, '   ')
      expect(state.signUpPassword).to.eql('')
    })
  })
})
