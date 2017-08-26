<template>
  <div class="box">
      <h1 class="title">«« _('Log in') »»</h2>
      <div class="columns is-centered">
        <div class="column">
          <login-form></login-form>
        </div>
      </div>
  </div>
</template>

<script>
import LoginForm from './LoginForm'

export default {
  name: 'login-page',
  components: {
    LoginForm
  }
}
</script>
