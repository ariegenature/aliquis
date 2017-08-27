<template>
 <div class="hero is-fullheight" id="sign-hero">
   <div class="hero-body">
     <div class="container">
       <div class="columns is-centered">
         <div class="column is-two-third">
           <div class="card">
             <div class="card-content">
               <div class="media">
                 <figure class="media-left">
                   <img src="http://ariegenature.fr/wp-content/uploads/2017/06/logoana_moy.png"
                        width="100"
                        alt="Logo ANA">
                 </figure>
                 <div class="media-content">
                   <h1 class="title is-size-4">«« _('Create Your ANA Account') »»</h1>
                 </div>
               </div>
               <sign-up-form></sign-up-form>
             </div>
             <footer class="card-footer">
               <p class="card-footer-item">
                 <span class="is-size-7">
                   «« _('Already have an account?') »»&thinsp;
                   <router-link :to="{ name: 'login' }">«« _('Log in!') »»</router-link>
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
import SignUpForm from './SignUpForm'

export default {
  name: 'sign-up-page',
  components: {
    SignUpForm
  }
}
</script>
