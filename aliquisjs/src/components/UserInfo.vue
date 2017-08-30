<template>
  <div class="card">
    <header class="card-header">
      <h3 class="card-header-title">«« _('Login information') »»</h3>
    </header>
    <div class="card-content">
      <div class="content">
        <dl>
          <dt>
          <b-icon :icon="isActive ? 'check-square-o' : 'warning'"
           :class="isActive ? '' : 'is-danger'"></b-icon>&thinsp;
          <span>«« _('Account:') »»</span>
          </dt>
          <dd :class="isActive ? 'has-text-success' : 'has-text-danger'">
          {{ isActive ? "«« _('active') »»" : "«« _('inactive') »»" }}
          </dd>
          <dt>
          <b-icon icon="user"></b-icon>&thinsp;<span>«« _('Your username:') »»</span>
          </dt>
          <b-tooltip label="«« _('Cannot be changed') »»" position="is-right" class="is-info">
            <dd><kbd class="has-text-info">{{ username }}</kbd></dd>
          </b-tooltip>
          <dt>
          <b-icon icon="envelope"></b-icon>&thinsp;<span>«« _('Your email address:') »»</span>
          </dt>
          <dd><kbd class="has-text-info">{{ email }}</kbd></dd>
        </dl>
      </div>
    </div>
    <div class="card-footer">
      <router-link :to="{ name: 'email', params: { username: username } }"
        class="card-footer-item is-size-7">
        <b-icon icon="envelope" size="is-small"></b-icon>&thinsp;
        <span>«« _('Change your email address') »»</span>
      </router-link>
      <router-link :to="{ name: 'password', params: { username: username} }"
        class="card-footer-item is-size-7">
        <b-icon icon="user-secret" size="is-small"></b-icon>&thinsp;
        <span>«« _('Change your password') »»</span>
      </router-link>
      </a>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'user-info',
  computed: mapGetters({
    'isActive': 'getIsActive',
    'username': 'getUsername',
    'email': 'getEmail'
  })
}
</script>
