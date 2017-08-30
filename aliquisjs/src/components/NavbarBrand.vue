<template>
  <div class="navbar-brand">
    <a class="navbar-item" href="/">
      <img src="/static/logo_ana.png" alt="Logo ANA">
    </a>
    <div class="navbar-burger burger" :class="{ 'is-active': menuActive }" @click="emitBurgerClick">
      <span></span>
      <span></span>
      <span></span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'navbar-brand',
  props: ['menuActive'],
  methods: {
    emitBurgerClick (ev) {
      this.$emit('burger-click')
    }
  }
}
</script>
