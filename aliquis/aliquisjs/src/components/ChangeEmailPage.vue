<template>
  <main class="section">
  <div class="container">
    <h1 class="title">«« _('Change your email address') »»</h1>
    <section class="section">
      <div class="container">
        <div class="columns is-centered">
          <div class="column">
            <change-email-form></change-email-form>
          </div>
          <div class="column">
            <change-email-info></change-email-info>
          </div>
        </div>
      </div>
    </section>
  </div>
  </main>
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
