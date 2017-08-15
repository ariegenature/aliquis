<template>
  <form id="sign-up-form" method="POST" accept-charset="UTF-8" @submit.prevent="submitForm">
    <div class="field is-horizontal">
      <div class="field-label">
        <label class="label is-normal">Your name</label>
      </div>
      <div class="field-body">
        <input-bound-input-field id="first_name"
                                 placeholder="First name"
                                 icon="user-o"
                                 autofocus
                                 required
                                 expanded
                                 :value="firstName"
                                 @input="updateFirstName"></input-bound-input-field>
        <input-bound-input-field id="surname"
                                 placeholder="Surname"
                                 icon="user-o"
                                 required
                                 expanded
                                 :value="surname"
                                 @input="updateSurname"></input-bound-input-field>
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label">
        <label class="label">Display name</label>
      </div>
      <div class="field-body">
        <input-bound-input-field id="display_name"
                                 help-message="How your name will be displayed in applications"
                                 icon="vcard-o"
                                 required
                                 :value="displayName"
                                 @input="updateDisplayName"></input-bound-input-field>
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label">
        <label class="label">Your email address</label>
      </div>
      <div class="field-body">
        <input-bound-input-field type="email"
                                 id="email"
                                 icon="envelope"
                                 required
                                 :value="email"
                                 @input="updateEmail"
                                 :validators="{regex: emailRegExp}"></input-bound-input-field>

      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label">
        <label class="label">Your credentials</label>
      </div>
      <div class="field-body">
        <input-bound-input-field id="username"
                                 help-message="Only lowercase letters and digits"
                                 placeholder="Username"
                                 icon="user"
                                 required
                                 :value="username"
                                 @input="updateUsername"
                                 :validators="{regex: usernameRegExp}"></input-bound-input-field>
        <input-bound-input-field type="password"
                                 id="password"
                                 help-message="At least 6 characters"
                                 placeholder="Password"
                                 icon="user-secret"
                                 required
                                 :value="password"
                                 @input="updatePassword"
                                 :validators="{min: 6}"></input-bound-input-field>
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label"></div>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <button class="button is-primary" type="submit" :disabled="!formReady"
                                              @submit.prevent="submitForm">
              Sign up
            </button>
          </div>
        </div>
      </div>
    </div>
    <b-loading :active.sync="isWaiting"></b-loading>
  </form>
</template>

<script>
import InputBoundInputField from './InputBoundInputField'
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'sign-up-form',
  components: {
    InputBoundInputField
  },
  data () {
    return {
      isWaiting: false
    }
  },
  computed: mapGetters({
    'firstName': 'getSignUpFirstName',
    'surname': 'getSignUpSurname',
    'displayName': 'getSignUpDisplayName',
    'email': 'getSignUpEmail',
    'username': 'getSignUpUsername',
    'password': 'getSignUpPassword',
    'emailRegExp': 'getEmailRegExp',
    'usernameRegExp': 'getUsernameRegExp',
    'formReady': 'validateSignUpData'
  }),
  methods: {
    submitForm (ev) {
      this.isWaiting = true
      var signUpData = new FormData()
      signUpData.append('first_name', this.firstName)
      signUpData.append('surname', this.surname)
      signUpData.append('display_name', this.displayName)
      signUpData.append('email', this.email)
      signUpData.append('username', this.username)
      signUpData.append('password', this.password)
      this.$http.post('', signUpData).then(response => {
        console.log(response)
      }, response => {
        console.log(response)
      })
      setTimeout(() => {
        this.isWaiting = false
      }, 3 * 1000)
    },
    ...mapActions({
      'updateFirstName': 'updateSignUpFirstName',
      'updateSurname': 'updateSignUpSurname',
      'updateDisplayName': 'updateSignUpDisplayName',
      'updateEmail': 'updateSignUpEmail',
      'updateUsername': 'updateSignUpUsername',
      'updatePassword': 'updateSignUpPassword'
    })
  }
}
</script>
