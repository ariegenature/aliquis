<template>
  <main class="section">
  <div class="container">
    <h1 class="title">«« _('Welcome') »» {{ firstName }}</h1>
    <section class="section">
      <div class="container">
        <div class="columns is-centered">
          <div class="column">
            <user-form></user-form>
          </div>
          <div class="column">
            <user-info></user-info>
          </div>
        </div>
        <hr>
        <div class="columns is-centered">
          <div class="column has-text-centered">
            <h2 class="subtitle has-text-weight-bold">«« _('Your services') »»</h2>
          </div>
        </div>
        <div class="columns is-centered" v-if="grants.length === 0">
          <div class="column">
            <div class="content has-text-centered">
              <p><b-icon icon="ban" type="is-warning"></b-icon>
              <span>«« _('You have not been granted any service') »»</span></p>
            </div>
          </div>
        </div>
        <div class="columns is-centered is-multiline" v-if="grants.length > 0">
          <div class="column is-one-third" v-for="grant in grants">
            <div class="content has-text-centered">
              <p><b-icon icon="check" type="is-success"></b-icon>
              <span>{{ grant }}</span></p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
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
    'firstName': 'getFirstName',
    'grants': 'getGrants'
  })
}
</script>
