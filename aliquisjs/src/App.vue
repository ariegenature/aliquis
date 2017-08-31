<template>
  <div id="app">
    <router-view name="navbar"></router-view>
    <router-view></router-view>
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
  watch: {
    statusMessage (val) {
      if (val) {
        this.$toast.open({
          message: val,
          type: this.statusMessageClass,
          duration: 8000
        })
      }
    }
  },
  mounted () {
    if (this.$route.params.username) {
      this.fetchAndInitUser(this.$route.params.username)
    }
  }
}
</script>
