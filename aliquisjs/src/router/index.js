import Vue from 'vue'
import Router from 'vue-router'
import ChangeEmailPage from '@/components/ChangeEmailPage'
import ChangePasswordPage from '@/components/ChangePasswordPage'
import ConfirmPage from '@/components/ConfirmPage'
import ErrorPage from '@/components/ErrorPage'
import LoginPage from '@/components/LoginPage'
import SignUpPage from '@/components/SignUpPage'
import UserPage from '@/components/UserPage'
import UserNavBar from '@/components/UserNavBar'

Vue.use(Router)

export default new Router({
  name: 'router',
  mode: 'history',
  routes: [
    {
      path: '/sign-up',
      name: 'sign-up',
      components: {
        default: SignUpPage
      }
    },
    {
      path: '/login',
      name: 'login',
      components: {
        default: LoginPage
      }
    },
    {
      path: '/user/:username',
      name: 'user',
      components: {
        navbar: UserNavBar,
        default: UserPage
      }
    },
    {
      path: '/email/:username',
      name: 'email',
      components: {
        navbar: UserNavBar,
        default: ChangeEmailPage
      }
    },
    {
      path: '/password/:username',
      name: 'password',
      components: {
        navbar: UserNavBar,
        default: ChangePasswordPage
      }
    },
    {
      path: '/error/:code(\\d+)',
      components: {
        default: ErrorPage
      }
    },
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/confirm/:token',
      name: 'confirm',
      components: {
        default: ConfirmPage
      }
    }
  ]
})
