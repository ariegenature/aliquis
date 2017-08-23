<template>
  <section>
    <h2 class="title">«« _('Change your password') »»</h2>
    <div class="columns is-centered">
      <div class="column">
        <change-password-form></change-password-form>
      </div>
      <div class="column">
        <change-password-info></change-password-info>
      </div>
    </div>
  </section>
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
