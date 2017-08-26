<template>
  <main class="section">
  <h1 class="title">«« _('Welcome') »» {{ firstName }}</h1>
  <section class="section">
    <div class="columns is-centered">
      <div class="column">
        <user-form></user-form>
      </div>
      <div class="column">
        <user-info></user-info>
      </div>
    </div>
  </section>
  </main>
</template>

<script>
import UserForm from './UserForm'
import UserInfo from './UserInfo'
import { mapGetters } from 'vuex'

export default {
  name: 'user-page',
  components: {
    UserForm,
    UserInfo
  },
  computed: mapGetters({
    'firstName': 'getFirstName'
  })
}
</script>
