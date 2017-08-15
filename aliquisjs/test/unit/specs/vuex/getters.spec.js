import getters from '../../../../src/vuex/getters'

describe('getters', () => {
  var state, mockGetters

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
    mockGetters = {
      getSignUpDisplayName: `${state.signUpFirstName} ${state.signUpSurname}`,
      getSignUpUsername: 'jdo' // no hardcoded 'jdo'
    }
  })

  describe('getSignUpFirstName', () => {
    it('should return first name used to sign up', () => {
      expect(getters.getSignUpFirstName(state)).to.eql(state.signUpFirstName)
    })
  })

  describe('getSignUpSurname', () => {
    it('should return surname used to sign up', () => {
      expect(getters.getSignUpSurname(state)).to.eql(state.signUpSurname)
    })
  })

  describe('getSignUpDisplayNameNotProvided', () => {
    it('should return first name and surname concatenation', () => {
      expect(getters.getSignUpDisplayName(state)).to.eql(
        `${state.signUpFirstName} ${state.signUpSurname}`
      )
    })
  })

  describe('getSignUpDisplayNameProvided', () => {
    it('should return provided display name', () => {
      state.signUpDisplayName = 'J. Doe'
      expect(getters.getSignUpDisplayName(state)).to.eql('J. Doe')
    })
  })

  describe('getSignUpDisplayNameOnlyFirstName', () => {
    it('should return first name', () => {
      state.signUpSurname = ''
      expect(getters.getSignUpDisplayName(state)).to.eql(state.signUpFirstName)
    })
  })

  describe('getSignUpDisplayNameOnlySurname', () => {
    it('should return surname', () => {
      state.signUpFirstName = ''
      expect(getters.getSignUpDisplayName(state)).to.eql(state.signUpSurname)
    })
  })

  describe('getSignUpDisplayNameEmpty', () => {
    it('should return empty string', () => {
      state.signUpFirstName = ''
      state.signUpSurname = ''
      expect(getters.getSignUpDisplayName(state)).to.eql('')
    })
  })

  describe('getSignUpEmail', () => {
    it('should return email used to sign up', () => {
      expect(getters.getSignUpEmail(state)).to.eql(state.signUpEmail)
    })
  })

  describe('getSignUpUsernameNotProvided', () => {
    it('should return concat: first letter of first name + surname without accents', () => {
      expect(getters.getSignUpUsername(state, mockGetters)).to.eql('jdo') // XXX: no hardcoded 'jdo'
    })
  })

  describe('getSignUpUsernameProvided', () => {
    it('should return provided user name (lowercase, only ascii letters and digits)', () => {
      state.signUpUsername = 'J-doé'
      expect(getters.getSignUpUsername(state, mockGetters)).to.eql('jdo')
    })
  })

  describe('getSignUpUsernameOnlyFirstName', () => {
    it('should return first name (lowercase, only ascii letters and digits)', () => {
      state.signUpSurname = ''
      expect(getters.getSignUpUsername(state)).to.eql(state.signUpFirstName.toLowerCase())
    })
  })

  describe('getSignUpUsernameOnlySurname', () => {
    it('should return surname (lowercase, only ascii letters and digits)', () => {
      state.signUpFirstName = ''
      expect(getters.getSignUpUsername(state)).to.eql('do') // XXX: no hardcoded 'do'
    })
  })

  describe('getSignUpUsernameEmpty', () => {
    it('should return empty string', () => {
      state.signUpFirstName = ''
      state.signUpSurname = ''
      expect(getters.getSignUpDisplayName(state)).to.eql('')
    })
  })

  describe('getSignUpPassword', () => {
    it('should return password used to sign up', () => {
      expect(getters.getSignUpPassword(state)).to.eql(state.signUpPassword)
    })
  })

  describe('getEmailRegExp', () => {
    it('should return E-mail regular expression', () => {
      expect(getters.getEmailRegExp(state)).to.eql(state.emailRegExp)
    })
  })

  describe('getUsernameRegExp', () => {
    it('should return username regular expression', () => {
      expect(getters.getUsernameRegExp(state)).to.eql(state.usernameRegExp)
    })
  })

  describe('validateSignUpDataOK', () => {
    it('should return true when all sign up data is fine', () => {
      expect(getters.validateSignUpData(state, mockGetters)).to.be.true
    })
  })

  describe('validateSignUpDataMissingFirstName', () => {
    it('should return false when first name is missing', () => {
      state.signUpFirstName = ''
      expect(getters.validateSignUpData(state, mockGetters)).to.be.false
    })
  })

  describe('validateSignUpDataMissingSurname', () => {
    it('should return false when surname is missing', () => {
      state.signUpSurname = ''
      expect(getters.validateSignUpData(state, mockGetters)).to.be.false
    })
  })

  describe('validateSignUpDataMissingDisplayName', () => {
    it('should return false when display name is missing', () => {
      mockGetters.getSignUpDisplayName = ''
      expect(getters.validateSignUpData(state, mockGetters)).to.be.false
    })
  })

  describe('validateSignUpDataEmptyEmail', () => {
    it('should return false when email is missing', () => {
      state.signUpEmail = ''
      expect(getters.validateSignUpData(state, mockGetters)).to.be.false
    })
  })

  describe('validateSignUpDataWrongEmail', () => {
    it('should return false when email is not valid', () => {
      state.signUpEmail = 'john'
      expect(getters.validateSignUpData(state, mockGetters)).to.be.false
    })
  })

  describe('validateSignUpDataEmptyUsername', () => {
    it('should return false when username is missing', () => {
      mockGetters.getSignUpUsername = ''
      expect(getters.validateSignUpData(state, mockGetters)).to.be.false
    })
  })

  describe('validateSignUpDataWrongUsername', () => {
    it('should return false when username is not valid', () => {
      mockGetters.getSignUpUsername = 'J-doé'
      expect(getters.validateSignUpData(state, mockGetters)).to.be.false
    })
  })

  describe('validateSignUpDataEmptyPassword', () => {
    it('should return false when password is empty', () => {
      state.signUpPassword = ''
      expect(getters.validateSignUpData(state, mockGetters)).to.be.false
    })
  })

  describe('validateSignUpDataWrongPassword', () => {
    it('should return false when password is too short', () => {
      state.signUpPassword = 'jdoe1'
      expect(getters.validateSignUpData(state, mockGetters)).to.be.false
    })
  })
})

