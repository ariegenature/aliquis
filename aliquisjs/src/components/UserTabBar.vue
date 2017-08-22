<template>
  <div class="tabs">
    <ul>
      <router-link :to="{ name: 'user', params: { username: username } }" tag="li"
        active-class="is-active">
        <a>{{ displayName }}</a>
      </router-link>
      <li><a href="«« url_for('sign.logout') »»">«« _('Log Out') »»</a></li>
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
