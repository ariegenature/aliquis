<template>
  <div class="tabs">
    <ul>
      <router-link :to="{name: 'login'}" tag="li" active-class="is-active">
        <a><b-icon icon="sign-in" size="is-small"></b-icon><span>«« _('Sign In') »»</span></a>
      </router-link>
      <router-link :to="{name: 'sign-up'}" tag="li" active-class="is-active">
        <a><b-icon icon="user-plus" size="is-small"></b-icon><span>«« _('Sign Up') »»</span></a>
      </router-link>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'sign-tab-bar'
}
</script>
