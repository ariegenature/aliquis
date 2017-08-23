<template>
  <section>
    <h2 class="title">«« _('Welcome') »» {{ firstName }}</h2>
    <div class="columns is-centered">
      <div class="column">
        <user-form></user-form>
      </div>
      <div class="column">
        <user-info></user-info>
      </div>
    </div>
  </section>
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
