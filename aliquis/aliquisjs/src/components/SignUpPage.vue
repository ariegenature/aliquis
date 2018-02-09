<template>
 <div class="hero is-fullheight" id="sign-hero">
   <div class="hero-body">
     <div class="container">
       <div class="columns is-centered is-1">
         <div class="column is-two-thirds">
           <div class="card">
             <div class="card-header">
               <div class="media-content">
                 <h1 class="card-header-title">«« _('Create Your ANA Account') »»</h1>
               </div>
               <div class="card-header-icon">
                 <img src="/static/logo_ana.png" width="64" alt="Logo ANA">
               </div>
             </div>
             <div class="card-content">
               <div class="columns is-8">
                 <div id="main-column" class="column">
                   <sign-up-form></sign-up-form>
                 </div>
                 <div id="switch-column" class="column is-narrow">
                   <div class="content has-text-centered is-size-7">
                     <p>«« _('Already have an account?') »»</p>
                     <p>
                     <router-link :to="{ name: 'login' }">
                       <b-icon icon="arrow-circle-right" size="is-small"></b-icon>
                       <span>«« _('Log in!') »»</span>
                     </router-link>
                     </p>
                   </div>
                 </div>
               </div>
             </div>
           </div>
         </div>
         <div class="column">
           <sign-up-info v-if="!passwordHelp"></sign-up-info>
         </div>
       </div>
     </div>
   </div>
 </div>
</template>

<script>
import SignUpForm from './SignUpForm'
import SignUpInfo from './SignUpInfo'

export default {
  name: 'sign-up-page',
  components: {
    SignUpForm,
    SignUpInfo
  }
}
</script>
