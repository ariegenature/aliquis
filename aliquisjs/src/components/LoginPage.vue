<template>
 <div class="hero is-fullheight" id="sign-hero">
   <div class="hero-body">
     <div class="container">
       <div class="columns is-centered">
         <div class="column is-one-third">
           <div class="card">
             <div class="card-content">
               <div class="media">
                 <figure class="media-left">
                   <img src="/static/logo_ana.png" width="100" alt="Logo ANA">
                 </figure>
                 <div class="media-content">
                   <h1 class="title is-size-4">«« _('Log in') »»</h1>
                 </div>
               </div>
               <login-form></login-form>
             </div>
             <footer class="card-footer">
               <p class="card-footer-item">
                 <span class="is-size-7">
                   «« _('No account yet?') »»&thinsp;
                   <router-link :to="{ name: 'sign-up' }">«« _('Sign up!') »»</router-link>
                 </span>
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
  background-image: url("http://ariegenature.fr/wp-content/uploads/2017/08/automne_bethmal.jpg");
}
#app .card {
  border-radius: 10px;
  background-color: #ffffffee;
}
</style>
