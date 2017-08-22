import Vue from 'vue'
import VueResource from 'vue-resource'

Vue.use(VueResource)

const UserResource = Vue.resource("«« url_for('home') »»" + 'api/user{/username}')

export default {
  fetchUser: (username) => {
    return UserResource.get({ username })
  },
  updateUser: (data) => {
    return UserResource.update({ username: data.username }, data)
  }
}
