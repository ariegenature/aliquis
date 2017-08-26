<template>
  <div id="app">
    <router-view name="navbar"></router-view>
    <div class="container">
      <b-notification :type="statusMessageClass" :active.sync="statusMessage"
         v-if="statusMessage">
        {{statusMessage}}
      </b-notification>
      <router-view></router-view>
    </div>
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
