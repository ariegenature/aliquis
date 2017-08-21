import Vue from 'vue'
import Router from 'vue-router'
import LoginPage from '@/components/LoginPage'
import SignTabBar from '@/components/SignTabBar'
import SignUpPage from '@/components/SignUpPage'

Vue.use(Router)

export default new Router({
  name: 'router',
  mode: 'history',
  routes: [
    {
      path: '/sign-up',
      name: 'sign-up',
      components: {
        tabbar: SignTabBar,
        default: SignUpPage
      }
    },
    {
      path: '/login',
      name: 'login',
      components: {
        tabbar: SignTabBar,
        default: LoginPage
      }
    },
    {
      path: '/',
      redirect: '/login'
    }
  ]
})
