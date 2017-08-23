<template>
  <div class="card">
    <header class="card-header">
      <h3 class="card-header-title">«« _('Security') »»</h3>
    </header>
    <div class="card-content">
      <div class="content">
        <p>«« _('For security reasons, we ask your current password again.') »»</p>
        <p>«« _('Also, please remember that the longer the password is, the better security it does provide.') »»</p>
        <p>«« _('A simple way to have a secure and easy to remember password is to choose four words.') »»</p>
        <p>«« _('For example:') »»&nbsp;<kbd>«« _('How_husband_determine_country') »»</kbd></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'change-password-info'
}
</script>
