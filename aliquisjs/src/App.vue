<template>
  <div id="app">
    <header class="hero is-fullheight">
      <div class="hero-body">
        <div class="container">
          <div class="columns is-centered">
            <div class="column">
              <b-notification :type="statusMessageClass" :active.sync="statusMessage"
                 v-if="statusMessage">
                {{statusMessage}}
              </b-notification>
              <div class="box">
                <router-view name="tabbar"></router-view>
                <router-view></router-view>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
    <b-loading :active.sync="isLoading"></b-loading>
  </div>
</template>

<script>
import store from './vuex/store'
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'app',
  store,
  computed: mapGetters({
    'statusMessage': 'getStatusMessage',
    'statusMessageClass': 'getStatusMessageClass',
    'isLoading': 'getIsLoading'
  }),
  methods: mapActions({
    'fetchAndInitUser': 'fetchAndInitUser'
  }),
  mounted () {
    this.fetchAndInitUser(this.$route.params.username)
  }
}
</script>
