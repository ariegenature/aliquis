<template>
  <div class="card">
    <header class="card-header">
      <h3 class="card-header-title">«« _('Why sign up?') »»</h3>
    </header>
    <div class="card-content">
      <div class="content">
        <p>«« _('By creating an account, you will be granted access to some services.') »»</p>
        <p>«« _('At the very least, you will be able to share your nature observations and thus contribute to common knowledge.') »»</p>
        <p>«« _('But depending on your needs, we might allow you to use other services, if it makes sense.') »»</p>
        <p><strong>«« _('About your credentials') »»</strong></p>
        <p>«« _('When you choose a new password, remember that the longer the password is, the better security it does provide.') »»</p>
        <p>«« _('A simple way to have a secure and easy to remember password is to choose four words.') »»</p>
        <p>«« _('For example:') »»&nbsp;<kbd>«« _('How_husband_determine_country') »»</kbd></p>
        <p>«« _('One final note about username. Once chosen, you cannot change your username.') »»</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'sign-up-info'
}
</script>
