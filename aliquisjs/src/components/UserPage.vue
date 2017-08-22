<template>
  <section>
    <h2 class="title">«« _('Welcome') »» {{ firstName }}</h2>
    <div class="columns is-centered">
      <div class="column">
        <user-form></user-form>
      </div>
    </div>
  </section>
</template>

<script>
import UserForm from './UserForm'
import { mapGetters } from 'vuex'

export default {
  name: 'user-page',
  components: {
    UserForm
  },
  computed: mapGetters({
    'firstName': 'getFirstName'
  })
}
</script>
