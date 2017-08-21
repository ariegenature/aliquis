<template>
  <div class="tabs">
    <ul>
      <router-link :to="{name: 'login'}" tag="li" active-class="is-active">
        <a>«« _('Sign In') »»</a>
      </router-link>
      <router-link :to="{name: 'sign-up'}" tag="li" active-class="is-active">
        <a>«« _('Sign Up') »»</a>
      </router-link>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'sign-tab-bar'
}
</script>
