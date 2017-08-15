import Vue from 'vue'
import Router from 'vue-router'
import SignUpPage from '@/components/SignUpPage'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/sign-up',
      name: 'sign-up',
      component: SignUpPage
    },
    {
      path: '/',
      redirect: '/sign-up'
    }
  ]
})
