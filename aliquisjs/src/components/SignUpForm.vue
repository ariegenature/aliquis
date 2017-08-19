<template>
  <form id="sign-up-form" method="POST" accept-charset="UTF-8" @submit.prevent="submitForm">
    <b-notification :type="formMessageClass" :active.sync="formMessage" v-if="formMessage">
      {{formMessage}}
    </b-notification>
    <div class="field is-horizontal">
      <div class="field-label">
        <label class="label is-normal">«« _('Your name') »»</label>
      </div>
      <div class="field-body">
        <input-bound-input-field id="first_name"
                                 :state="inputState"
                                 placeholder="«« form.first_name.label.text »»"
                                 icon="user-o"
                                 autofocus
                                 required
                                 expanded
                                 :value="firstName"
                                 @input="updateFirstName"></input-bound-input-field>
        <input-bound-input-field id="surname"
                                 :state="inputState"
                                 placeholder="«« form.surname.label.text »»"
                                 icon="user-o"
                                 required
                                 expanded
                                 :value="surname"
                                 @input="updateSurname"></input-bound-input-field>
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label">
        <label class="label">«« form.display_name.label.text »»</label>
      </div>
      <div class="field-body">
        <input-bound-input-field id="display_name"
                                 :state="inputState"
                                 help-message="«« form.display_name.description »»"
                                 icon="vcard-o"
                                 required
                                 :value="displayName"
                                 @input="updateDisplayName"></input-bound-input-field>
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label">
        <label class="label">«« _('Your email address') »»</label>
      </div>
      <div class="field-body">
        <input-bound-input-field type="email"
                                 id="email"
                                 :state="inputState"
                                 icon="envelope"
                                 required
                                 :value="email"
                                 @input="updateEmail"
                                 :validators="{regex: emailRegExp}"></input-bound-input-field>

      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label">
        <label class="label">«« _('Your credentials') »»</label>
      </div>
      <div class="field-body">
        <input-bound-input-field id="username"
                                 :state="inputState"
                                 placeholder="«« form.username.label.text »»"
                                 help-message="«« form.username.description »»"
                                 icon="user"
                                 required
                                 :value="username"
                                 @input="updateUsername"
                                 :validators="{regex: usernameRegExp}"></input-bound-input-field>
        <input-bound-input-field type="password"
                                 id="password"
                                 :state="inputState"
                                 placeholder="«« form.password.label.text »»"
                                 help-message="«« form.password.description »»"
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
              «« _('Go!') »»
            </button>
          </div>
        </div>
        <div class="field">
          <div class="control">
            <input type="hidden" name="csrf_token" value="«« csrf_token() »»">
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
      isWaiting: false,
      formMessage: '',
      formMessageClass: '',
      inputState: {
        'first_name': '',
        'surname': '',
        'display_name': '',
        'email': '',
        'username': '',
        'password': ''
      }
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
      this.$http.post('', signUpData,
        {headers: {'X-CSRFToken': '«« csrf_token() »»'}}).then(response => {
          this.isWaiting = false
          this.formMessage = 'Your information has been saved. You will soon receive an email to ' +
            'confirm your registration'
          this.formMessageClass = 'is-success'
          for (var inputId in this.inputState) {
            this.inputState[inputId] = 'is-success'
          }
        }, response => {
          this.isWaiting = false
          this.formMessageClass = 'is-danger'
          if (response.status === 500 || response.status === 400) {
            if (response.status === 500) {
              this.formMessage = "«« _('A technical problem occured. Please contact helpdesk@ariegenature.fr for assistance') »»"
            }
            if (response.status === 400) {
              this.formMessage = 'Delay expired, please refresh the page'
            }
            for (var inputId in this.inputState) {
              this.inputState[inputId] = ''
            }
          }
          if (response.status === 409) {
            var errorJson = response.body
            this.formMessage = errorJson.message
            errorJson.errors.forEach((err) => {
              this.inputState[err.field] = 'is-danger'
            })
          }
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
