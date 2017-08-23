<template>
  <form id="change-password-form" method="POST" accept-charset="UTF-8" @submit.prevent="submitForm">
    <input-bound-input-field id="current_password"
                             type="password"
                             placeholder="«« _('Current password') »»"
                             :state="inputState"
                             icon="user-secret"
                             autofocus
                             required
                             v-model="currentPassword"></input-bound-input-field>
    <input-bound-input-field id="new_password"
                             type="password"
                             :state="inputState"
                             placeholder="«« _('New password') »»"
                             help-message="«« _('At least 6 characters') »»"
                             icon="user-secret"
                             required
                             v-model="newPassword"
                             :validators="{min: 6}"></input-bound-input-field>
    <b-field :type="passwordConfirm === newPassword ? 'is-success' : 'is-danger'"
                             :message="passwordConfirmHelp">
      <b-input id="password_confirm"
               placeholder="«« _('New password confirm') »»"
               type="password"
               icon="user-secret"
               required="true"
               v-model="passwordConfirm"></b-input>
    </b-field>
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
  </form>
</template>

<script>
import InputBoundInputField from './InputBoundInputField'

export default {
  name: 'change-password-form',
  components: {
    InputBoundInputField
  },
  data () {
    return {
      currentPassword: '',
      newPassword: '',
      passwordConfirm: '',
      inputState: {
        'current_password': '',
        'new_password': ''
      }
    }
  },
  computed: {
    passwordConfirmHelp () {
      return this.passwordConfirm === this.newPassword ? '' : "«« _('Passwords do not match') »»"
    },
    formReady () {
      return this.currentPassword && this.newPassword.length >= 6 &&
        this.passwordConfirm === this.newPassword
    }
  },
  methods: {
    submitForm (ev) {
      this.setPageLoading()
      var statusClass = 'is-success'
      var formData = new FormData()
      formData.append('new_email', this.newEmail)
      this.$http.post('', formData,
        {headers: {'X-CSRFToken': '«« csrf_token() »»'}}).then(response => {
          this.setPageNotLoading()
          this.updateStatusMessage({
            msg: "«« _('Your password has been changed successfully.') »»",
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
    }
  }
}
</script>
