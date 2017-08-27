<template>
  <nav class="navbar has-shadow">
    <navbar-brand :menu-active="menuActive" @burger-click="toggleMenu"></navbar-brand>
    <div class="navbar-menu"  :class="{ 'is-active': menuActive }">
      <div class="navbar-start">
        <router-link :to="{ name: 'user', params: { username: username } }"
           class="navbar-item" active-class="is-active" @click.native="closeMenu">
          <b-icon icon="address-card" size="is-small"></b-icon>&thinsp;
          <span>{{ displayName }}</span>
        </router-link>
        <router-link :to="{ name: 'email', params: { username: username } }"
                                      class="navbar-item" active-class="is-active"
                                                          @click.native="closeMenu">
          <b-icon icon="envelope" size="is-small"></b-icon>&thinsp;
          <span>«« _('Email') »»</span>
        </router-link>
        <router-link :to="{ name: 'password', params: { username: username } }"
                                  class="navbar-item" active-class="is-active"
                                                      @click.native="closeMenu">
          <b-icon icon="user-secret" size="is-small"></b-icon>&thinsp;
          <span>«« _('Password') »»</span>
        </router-link>
      </div>
      <div class="navbar-end">
        <a href="«« url_for('sign.logout') »»" class="navbar-item">
          <b-icon icon="sign-out" size="is-small"></b-icon>&thinsp;
          <span>«« _('Log Out') »»</span>
        </a>
      </div>
    </div>
  </nav>
</template>

<script>
import NavbarBrand from './NavbarBrand'
import { mapGetters } from 'vuex'

export default {
  name: 'user-navbar',
  components: {
    NavbarBrand
  },
  data () {
    return {
      menuActive: false
    }
  },
  computed: mapGetters({
    'displayName': 'getDisplayName',
    'username': 'getUsername'
  }),
  methods: {
    toggleMenu () {
      this.menuActive = !this.menuActive
    },
    closeMenu () {
      this.menuActive = false
    }
  }
}
</script>

<style>
#app .navbar {
  background-color: #e9e5ff;
}
#app a.navbar-item:hover {
  background-color: #b4b0cb;
}
a.navbar-item.is-active {
  border-bottom-style: solid;
  border-bottom-width: 3px;
}
</style>
