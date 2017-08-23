import Vue from 'vue'
import Router from 'vue-router'
import ChangeEmailPage from '@/components/ChangeEmailPage'
import ChangePasswordPage from '@/components/ChangePasswordPage'
import LoginPage from '@/components/LoginPage'
import SignTabBar from '@/components/SignTabBar'
import SignUpPage from '@/components/SignUpPage'
import UserPage from '@/components/UserPage'
import UserTabBar from '@/components/UserTabBar'

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
      path: '/user/:username',
      name: 'user',
      components: {
        tabbar: UserTabBar,
        default: UserPage
      }
    },
    {
      path: '/change-email',
      name: 'change-email',
      components: {
        tabbar: UserTabBar,
        default: ChangeEmailPage
      }
    },
    {
      path: '/change-password',
      name: 'change-password',
      components: {
        tabbar: UserTabBar,
        default: ChangePasswordPage
      }
    },
    {
      path: '/',
      redirect: '/login'
    }
  ]
})
