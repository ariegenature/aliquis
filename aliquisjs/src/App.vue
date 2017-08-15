<template>
  <div id="app">
    <img src="./assets/logo.png">
    <router-view></router-view>
  </div>
</template>

<script>
import store from './vuex/store'

export default {
  name: 'app',
  store
}
</script>
