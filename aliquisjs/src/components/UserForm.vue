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
      <div class="field-label"></div>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <input type="hidden" name="csrf_token" value="«« csrf_token() »»">
          </div>
        </div>
        <div class="field">
          <div class="control">
            <button class="button is-primary" type="submit" :disabled="!formReady"
                                              @submit.prevent="submitForm">
              «« _('Update') »»
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
  name: 'user-form',
  components: {
    InputBoundInputField
  },
  data () {
    return {
      inputState: {
        'first_name': '',
        'surname': '',
        'display_name': ''
      }
    }
  },
  computed: {
    formReady () {
      return this.validateUserData
    },
    ...mapGetters({
      'firstName': 'getFirstName',
      'surname': 'getSurname',
      'displayName': 'getDisplayName',
      'username': 'getUsername',
      'isLoading': 'getIsLoading',
      'validateUserData': 'validateUserData'
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
      this.$http.post('', signUpData,
        {headers: {'X-CSRFToken': '«« csrf_token() »»'}}).then(response => {
          this.setPageNotLoading()
          this.updateStatusMessage({
            msg: "«« _('Your modifications have been saved.') »»",
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
          if (response.status === 401) {
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
      'fetchAndInitUser': 'fetchAndInitUser',
      'updateFirstName': 'updateFirstName',
      'updateSurname': 'updateSurname',
      'updateDisplayName': 'updateDisplayName',
      'updateStatusMessage': 'updateStatusMessage',
      'setPageLoading': 'setPageLoading',
      'setPageNotLoading': 'setPageNotLoading'
    })
  },
  mounted () {
    this.fetchAndInitUser(this.$route.params.username)
  }
}
</script>
