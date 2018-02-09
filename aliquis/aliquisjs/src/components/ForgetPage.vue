<template>
 <div class="hero is-fullheight" id="sign-hero">
   <div class="hero-body">
     <div class="container">
       <div class="columns is-centered">
         <div class="column is-two-thirds">
           <div class="card">
             <div class="card-header">
               <div class="media-content">
                 <h1 class="card-header-title">«« _('Reset your password') »»</h1>
               </div>
               <div class="card-header-icon">
                 <img src="/static/logo_ana.png" width="64" alt="Logo ANA">
               </div>
             </div>
             <div class="card-content">
               <div class="columns is-8">
                 <div id="main-column" class="column">
                   <forget-form></forget-form>
                 </div>
                 <div id="switch-column" class="column is-narrow">
                   <div class="content has-text-centered is-size-7">
                     <p>«« _('Back to') »»</p>
                     <p>
                     <router-link :to="{ name: 'login' }">
                       <b-icon icon="arrow-circle-left" size="is-small"></b-icon>
                       <span>«« _('Login page') »»</span>
                     </router-link>
                     </p>
                   </div>
                 </div>
               </div>
             </div>
           </div>
         </div>
       </div>
     </div>
   </div>
 </div>
</template>

<script>
import ForgetForm from './ForgetForm'

export default {
  name: 'reset-page',
  components: {
    ForgetForm
  }
}
</script>
