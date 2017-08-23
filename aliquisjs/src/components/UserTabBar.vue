<template>
  <div class="tabs">
    <ul>
      <router-link :to="{ name: 'user', params: { username: username } }" tag="li"
        active-class="is-active">
        <a><b-icon icon="address-card" size="is-small"></b-icon><span>{{ displayName }}</span></a>
      </router-link>
      <router-link :to="{ name: 'change-email' }" tag="li" active-class="is-active">
        <a><b-icon icon="envelope" size="is-small"></b-icon><span>«« _('Email') »»</span></a>
      </router-link>
      <li>
        <a href="«« url_for('sign.logout') »»">
          <b-icon icon="sign-out" size="is-small"></b-icon><span>«« _('Log Out') »»</span>
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'user-tab-bar',
  computed: mapGetters({
    'displayName': 'getDisplayName',
    'username': 'getUsername'
  })
}
</script>
