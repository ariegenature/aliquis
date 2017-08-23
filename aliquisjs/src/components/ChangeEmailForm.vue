<template>
  <form id="sign-up-form" method="POST" accept-charset="UTF-8" @submit.prevent="submitForm">
    <div class="field">
      <div class="control">
        <input type="hidden" name="csrf_token" value="«« csrf_token() »»">
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-body">
        <input-bound-input-field id="email"
                                 type="email"
                                 placeholder="«« _('New email address') »»"
                                 :state="inputState"
                                 icon="envelope"
                                 autofocus
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
      inputState: {
        'email': ''
      }
    }
  },
  computed: {
    formReady () {
      return this.newEmail.match(this.emailRegExp)
    },
    ...mapGetters({
      'newEmail': 'getNewEmail',
      'emailRegExp': 'getEmailRegExp'
    })
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
            msg: "«« _('You will soon receive an email to confirm your new address.') »»",
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
      'updateNewEmail': 'updateNewEmail'
    })
  }
}
</script>
