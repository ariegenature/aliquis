<template>
  <div id="app">
    <header class="hero">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">Your ANA account</h1>
        </div>
      </div>
    </header>
    <main class="section">
    <div class="container">
      <div class="columns is-centered">
        <div class="column">
          <div class="box">
            <router-view></router-view>
          </div>
        </div>
      </div>
    </div>
    </main>
  </div>
</template>

<script>
import store from './vuex/store'

export default {
  name: 'app',
  store
}
</script>
