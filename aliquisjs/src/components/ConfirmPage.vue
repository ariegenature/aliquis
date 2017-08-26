<template>
  <section>
    <div class="content">
      <p>«« _('Go back to') »»&nbsp;<a href="/">«« _('homepage') »»</a></p>
    </div>
  </section>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'confirm-page',
  methods: mapActions({
    'confirmUser': 'confirmUser'
  }),
  mounted () {
    this.confirmUser(this.$route.params.token)
  }
}
</script>
