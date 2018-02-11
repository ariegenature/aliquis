import Vue from 'vue'
import VueResource from 'vue-resource'

Vue.use(VueResource)

const UserResource = Vue.resource("«« url_for('home') »»" + 'api/user{/username}')
const ConfirmResource = Vue.resource("«« url_for('home') »»" + 'api/confirm{/token}')
const ReactivateResource = Vue.resource("«« url_for('home') »»" + 'api/reactivate{/username}')

export default {
  fetchUser: (username) => {
    return UserResource.get({ username })
  },
  updateUser: (data) => {
    return UserResource.update({ username: data.username }, data)
  },
  confirmUser: (token) => {
    return ConfirmResource.get({ token })
  },
  reactivateUser: (username) => {
    return ReactivateResource.get({ username })
  }
}
