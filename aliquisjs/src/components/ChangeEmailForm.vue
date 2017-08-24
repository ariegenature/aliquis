<template>
  <form id="change-email-form" method="POST" accept-charset="UTF-8" @submit.prevent="submitForm">
    <div class="field">
      <div class="control">
        <input type="hidden" name="csrf_token" value="«« csrf_token() »»">
      </div>
    </div>
    <input-bound-input-field id="current_password"
                             type="password"
                             placeholder="«« _('Current password') »»"
                             :state="inputState"
                             icon="user-secret"
                             autofocus
                             required
                             v-model="currentPassword"></input-bound-input-field>
    <div class="field is-horizontal">
      <div class="field-body">
        <input-bound-input-field id="new_email"
                                 type="email"
                                 placeholder="«« _('New email address') »»"
                                 :state="inputState"
                                 icon="envelope"
                                 required
                                 :value="newEmail"
                                 @input="updateNewEmail"
                                 :validators="{regex: emailRegExp}"></input-bound-input-field>
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
  name: 'change-email-form',
  components: {
    InputBoundInputField
  },
  data () {
    return {
      currentPassword: '',
      inputState: {
        'current_password': '',
        'new_email': ''
      }
    }
  },
  computed: {
    formReady () {
      return this.currentPassword && this.newEmail.match(this.emailRegExp)
    },
    ...mapGetters({
      'username': 'getUsername',
      'newEmail': 'getNewEmail',
      'emailRegExp': 'getEmailRegExp'
    })
  },
  methods: {
    clearChangeEmailData () {
      this.currentPassword = ''
      this.updateNewEmail('')
    },
    submitForm (ev) {
      this.setPageLoading()
      var statusClass = 'is-success'
      var formData = new FormData()
      formData.append('current_password', this.currentPassword)
      formData.append('new_email', this.newEmail)
      this.$http.post('', formData,
        {headers: {'X-CSRFToken': '«« csrf_token() »»'}}).then(response => {
          this.setPageNotLoading()
          this.updateStatusMessage({
            msg: "«« _('You will soon receive an email to confirm your new address.') »»",
            cls: statusClass
          })
          for (var inputId in this.inputState) {
            this.inputState[inputId] = statusClass
          }
          this.updateEmail(this.newEmail)
          this.clearChangeEmailData()
          this.$router.push({ name: 'user', params: {username: this.username} })
        }, response => {
          this.setPageNotLoading()
          statusClass = 'is-danger'
          if (response.status === 500) {
            this.updateStatusMessage({
              msg: "«« _('A technical problem occured. Please contact helpdesk@ariegenature.fr for assistance.') »»",
              cls: statusClass
            })
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
      'updateNewEmail': 'updateNewEmail',
      'updateEmail': 'updateEmail',
      'setPageLoading': 'setPageLoading',
      'setPageNotLoading': 'setPageNotLoading',
      'updateStatusMessage': 'updateStatusMessage'
    })
  }
}
</script>
