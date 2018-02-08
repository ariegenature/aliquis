<template>
  <form id="sign-up-form" method="POST" accept-charset="UTF-8" @submit.prevent="submitForm">
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
                                 :validators="{
                                 min: 6,
                                 not_in: ['How_husband_determine_country',
                                 'Comment_mari_determine_pays']
                                 }"></input-bound-input-field>
        <b-field :type="passwordConfirm === password ? 'is-success' : 'is-danger'"
                                 :message="passwordConfirmHelp">
          <b-input id="password_confirm"
                   placeholder="«« _('Password confirm') »»"
                   type="password"
                   icon="user-secret"
                   required="true"
                   v-model="passwordConfirm"></b-input>
        </b-field>
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label"></div>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <input type="hidden" name="csrf_token" value="«« csrf_token() »»">
          </div>
        </div>
        <div class="field">
          <div class="control">
            <input type="hidden" id="age" name="age" v-model="age">
          </div>
        </div>
        <div class="field">
          <div class="control">
            <button class="button is-primary" type="submit" :disabled="!formReady"
                                              @submit.prevent="submitForm">
              «« _('Go!') »»
            </button>
          </div>
        </div>
      </div>
    </div>
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
      passwordConfirm: '',
      age: '',
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
  computed: {
    passwordConfirmHelp () {
      return this.passwordConfirm === this.password ? '' : "«« _('Passwords do not match') »»"
    },
    formReady () {
      return this.validateSignUpData && this.passwordConfirm === this.password && !this.age
    },
    ...mapGetters({
      'firstName': 'getSignUpFirstName',
      'surname': 'getSignUpSurname',
      'displayName': 'getSignUpDisplayName',
      'email': 'getSignUpEmail',
      'username': 'getSignUpUsername',
      'password': 'getSignUpPassword',
      'emailRegExp': 'getEmailRegExp',
      'usernameRegExp': 'getUsernameRegExp',
      'validateSignUpData': 'validateSignUpData'
    })
  },
  methods: {
    submitForm (ev) {
      this.setPageLoading()
      var statusClass = 'is-success'
      var signUpData = new FormData()
      signUpData.append('first_name', this.firstName)
      signUpData.append('surname', this.surname)
      signUpData.append('display_name', this.displayName)
      signUpData.append('email', this.email)
      signUpData.append('username', this.username)
      signUpData.append('password', this.password)
      this.$http.post('', signUpData,
        {headers: {'X-CSRFToken': '«« csrf_token() »»'}}).then(response => {
          this.setPageNotLoading()
          this.updateStatusMessage({
            msg: "«« _('Your information has been saved. You will soon receive an email to confirm your registration.') »»",
            cls: statusClass
          })
          for (var inputId in this.inputState) {
            this.inputState[inputId] = statusClass
          }
          this.clearSignUpData()
          this.$router.push({ name: 'login' })
        }, response => {
          this.setPageNotLoading()
          statusClass = 'is-danger'
          if (response.status === 500 || response.status === 400) {
            if (response.status === 500) {
              this.updateStatusMessage({
                msg: "«« _('A technical problem occured. Please contact helpdesk@ariegenature.fr for assistance.') »»",
                cls: statusClass
              })
            }
            if (response.status === 400) {
              this.updateStatusMessage({
                msg: "«« _('Delay expired, please refresh the page.') »»",
                cls: statusClass
              })
            }
            for (var inputId in this.inputState) {
              this.inputState[inputId] = ''
            }
          }
          if (response.status === 409) {
            var errorJson = response.body
            this.updateStatusMessage({
              msg: errorJson.message,
              cls: statusClass
            })
            errorJson.errors.forEach((err) => {
              this.inputState[err.field] = statusClass
            })
          }
        })
      setTimeout(() => {
        this.setPageNotLoading()
      }, 3 * 1000)
    },
    ...mapActions({
      'updateFirstName': 'updateSignUpFirstName',
      'updateSurname': 'updateSignUpSurname',
      'updateDisplayName': 'updateSignUpDisplayName',
      'updateEmail': 'updateSignUpEmail',
      'updateUsername': 'updateSignUpUsername',
      'updatePassword': 'updateSignUpPassword',
      'clearSignUpData': 'clearSignUpData',
      'updateStatusMessage': 'updateStatusMessage',
      'setPageLoading': 'setPageLoading',
      'setPageNotLoading': 'setPageNotLoading'
    })
  }
}
</script>
