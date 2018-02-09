<template>
 <div class="hero is-fullheight" id="sign-hero">
   <div class="hero-body">
     <div class="container">
       <div class="columns is-centered">
         <div class="column is-half">
           <div class="card">
             <div class="card-header">
               <div class="media-content">
                 <h1 class="card-header-title">«« _('Log in') »»</h1>
               </div>
               <div class="card-header-icon">
                 <img src="/static/logo_ana.png" width="64" alt="Logo ANA">
               </div>
             </div>
             <div class="card-content">
               <div class="columns is-8">
                 <div id="main-column" class="column">
                   <login-form></login-form>
                 </div>
                 <div id="switch-column" class="column is-narrow">
                   <div class="content has-text-centered is-size-7">
                     <p>«« _('No account yet?') »»</p>
                     <p>
                     <router-link :to="{ name: 'sign-up' }">
                       <b-icon icon="arrow-circle-right" size="is-small"></b-icon>
                       <span>«« _('Sign up!') »»</span>
                     </router-link>
                     </p>
                   </div>
                 </div>
               </div>
             </div>
             <footer class="card-footer">
               <p class="card-footer-item is-size-7">
               <router-link :to="{ name: 'forget' }">
                 <b-icon icon="question-circle" size="is-small"></b-icon>
                 <span>«« _('Password forgotten?') »»</span>
               </router-link>
               </p>
             </footer>
           </div>
         </div>
       </div>
     </div>
   </div>
 </div>
</template>

<script>
import LoginForm from './LoginForm'

export default {
  name: 'login-page',
  components: {
    LoginForm
  }
}
</script>

<style>
#sign-hero {
  background-image: url("/static/automne_bethmal.jpg");
}
#app .card {
  border-radius: 10px;
  background-color: #ffffffee;
}
#main-column {
  border-right: thin solid #ddd;
}
#switch-column {
  margin-top: auto;
  margin-bottom: auto;
}
</style>
