<template>
  <form id="login-form" method="POST" accept-charset="UTF-8" @submit.prevent="submitForm">
    <b-field :type="inputState" label="«« form.username.label.text »»">
      <b-input id="username" icon="user" autofocus="true" v-model="username"></b-input>
    </b-field>
    <b-field :type="inputState" label="«« form.password.label.text »»">
      <b-input id="password" type="password" icon="user-secret" v-model="password"></b-input>
    </b-field>
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
import { mapActions } from 'vuex'

export default {
  name: 'login-form',
  components: {
    InputBoundInputField
  },
  data () {
    return {
      username: '',
      password: '',
      inputState: ''
    }
  },
  computed: {
    formReady () {
      return Boolean(this.username) && Boolean(this.password)
    }
  },
  methods: {
    submitForm (ev) {
      this.setPageLoading()
      var loginData = new FormData()
      loginData.append('username', this.username)
      loginData.append('password', this.password)
      this.$http.post('', loginData,
        {headers: {'X-CSRFToken': '«« csrf_token() »»'}}).then(response => {
          this.setPageNotLoading()
          this.inputState = 'is-success'
          this.clearStatusMessage()
          this.fetchAndInitUser(this.username)
          this.$router.push({ name: 'user', params: { username: this.username } })
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
