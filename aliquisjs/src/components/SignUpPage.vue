<template>
  <section>
      <h2 class="title">Sign Up</h2>
      <div class="columns is-centered">
        <div class="column">
          <sign-up-form></sign-up-form>
        </div>
      </div>
  </section>
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
