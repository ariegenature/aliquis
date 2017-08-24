<template>
  <div class="card">
    <header class="card-header">
      <h3 class="card-header-title">«« _('How to change your email address ?') »»</h3>
    </header>
    <div class="card-content">
      <div class="content">
        <p>«« _('For security reasons, we ask your current password again.') »»</p>
        <p><strong>«« _('Important:') »»</strong>&nbsp;<span>«« _('Updating your email address will deactivate your account until you activate it again.') »»</span></p>
        <p>«« _('After updating your email address with the opposite form, you will receive an e-mail at the new address. This email contains a link.') »»</p>
        <p>«« _('Just click on the link to confirm that this address belongs to you.') »»</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'change-email-info'
}
</script>
