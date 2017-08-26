<template>
  <nav class="navbar">
    <navbar-brand :menu-active="menuActive" @burger-click="toggleMenu"></navbar-brand>
    <div class="navbar-menu"  :class="{ 'is-active': menuActive }">
      <div class="navbar-start">
      </div>
      <div class="navbar-end">
        <router-link :to="{name: 'login'}" class="navbar-item" active-class="is-active"
                                                               @click.native="closeMenu">
          <b-icon icon="sign-in" size="is-small"></b-icon>&thinsp;
          <span>«« _('Sign In') »»</span>
        </router-link>
        <router-link :to="{name: 'sign-up'}" class="navbar-item" active-class="is-active"
                                                                 @click.native="closeMenu">
          <b-icon icon="user-plus" size="is-small"></b-icon>&thinsp;
          <span>«« _('Sign Up') »»</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script>
import NavbarBrand from './NavbarBrand'
export default {
  name: 'sign-navbar',
  components: {
    NavbarBrand
  },
  data () {
    return {
      menuActive: false
    }
  },
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
