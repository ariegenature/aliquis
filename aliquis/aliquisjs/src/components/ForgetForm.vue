<template>
  <form id="reset-form" method="POST" accept-charset="UTF-8" @submit.prevent="submitForm">
    <b-field>
      <input type="hidden" name="csrf_token" value="«« csrf_token() »»">
    </b-field>
    <b-field :type="inputState">
      <b-input id="email" icon="envelope" autofocus="true" v-model="email"
               expanded placeHolder="«« _('Your email address') »» "></b-input>
      <div class="control">
        <button class="button is-primary" type="submit" :disabled="!formReady"
                                          @submit.prevent="submitForm">
          «« _('Send') »»
        </button>
      </div>
    </b-field>
  </form>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'reset-form',
  data () {
    return {
      email: '',
      inputState: ''
    }
  },
  computed: {
    formReady () {
      return Boolean(this.email)
    }
  },
  methods: {
    submitForm (ev) {
      this.setPageLoading()
      var resetData = new FormData()
      resetData.append('email', this.email)
      this.$http.post('', resetData,
        {headers: {'X-CSRFToken': '«« csrf_token() »»'}}).then(response => {
          this.setPageNotLoading()
          this.inputState = 'is-success'
          this.updateStatusMessage({
            msg: "«« _('You will soon receive an email with instructions to change your password.') »»",
            cls: 'is-info'
          })
          this.$router.push({ name: 'login' })
        }, response => {
          this.setPageNotLoading()
          this.inputState = 'is-danger'
          if (response.status === 500) {
            this.updateStatusMessage({
              msg: "«« _('A technical problem occured. Please contact helpdesk@ariegenature.fr for assistance.') »»",
              cls: this.inputState
            })
          }
          if (response.status === 401) {
            this.updateStatusMessage({
              msg: response.body.message,
              cls: this.inputState
            })
          }
        })
      setTimeout(() => {
        this.setPageNotLoading()
      }, 3 * 1000)
    },
    ...mapActions({
      'fetchAndInitUser': 'fetchAndInitUser',
      'updateStatusMessage': 'updateStatusMessage',
      'clearStatusMessage': 'clearStatusMessage',
      'setPageLoading': 'setPageLoading',
      'setPageNotLoading': 'setPageNotLoading'
    })
  }
}
</script>
