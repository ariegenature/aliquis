<template>
  <div class="box">
      <h1 class="title">«« _('Create Your ANA Account') »»</h2>
      <div class="columns is-centered">
        <div class="column">
          <sign-up-form></sign-up-form>
        </div>
      </div>
  </div>
</template>

<script>
import SignUpForm from './SignUpForm'

export default {
  name: 'sign-up-page',
  components: {
    SignUpForm
  }
}
</script>
