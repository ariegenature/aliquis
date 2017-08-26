<template>
  <div class="section">
    <h2 class="title">«« _('Change your email address') »»</h2>
    <div class="columns is-centered">
      <div class="column">
        <change-email-form></change-email-form>
      </div>
      <div class="column">
        <change-email-info></change-email-info>
      </div>
    </div>
  </section>
</template>

<script>
import ChangeEmailForm from './ChangeEmailForm'
import ChangeEmailInfo from './ChangeEmailInfo'

export default {
  name: 'user-page',
  components: {
    ChangeEmailForm,
    ChangeEmailInfo
  }
}
</script>
