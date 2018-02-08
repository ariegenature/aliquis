<template>
  <main class="section">
  <div class="container">
    <h1 class="title">«« _('Change your password') »»</h1>
    <section class="section">
      <div class="container">
        <div class="columns is-centered">
          <div class="column">
            <change-password-form></change-password-form>
          </div>
          <div class="column">
            <change-password-info></change-password-info>
          </div>
        </div>
      </div>
    </section>
  </div>
  </main>
</template>

<script>
import ChangePasswordForm from './ChangePasswordForm'
import ChangePasswordInfo from './ChangePasswordInfo'

export default {
  name: 'user-page',
  components: {
    ChangePasswordForm,
    ChangePasswordInfo
  }
}
</script>
