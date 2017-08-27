<template>
 <div class="hero is-fullheight" id="sign-hero">
   <div class="hero-body">
     <div class="container">
       <div class="columns is-centered">
         <div class="column is-one-third">
           <div class="card">
             <header class="card-header">
               <h1 class="card-header-title">«« _('Sorry') »»</h1>
               <span class="card-header-icon">
                 <b-icon icon="frown-o"></b-icon>
               </span>
             </header>
             <div class="card-content">
               <div class="media">
                 <figure class="media-left">
                   <img src="http://ariegenature.fr/wp-content/uploads/2017/06/logoana_moy.png"
                        width="100"
                        alt="Logo ANA">
                 </figure>
                 <div class="media-content">
                   <h1 class="title">«« _('Error') »»&thinsp;{{ errorCode }}</h1>
                 </div>
               </div>
               <div class="content">
                 <p v-if="errorCode === 404">
                 «« _('Unable to find what you asked for.') »»
                 </p>
                 <p v-if="errorCode === 403">
                 «« _('You are not allowed to access this resource.') »»
                 </p>
                 <p v-if="errorCode === 500">
                 «« _('A technical problem occured. Please contact helpdesk@ariegenature.fr for assistance.') »»
                 </p>
               </div>
             </div>
             <footer class="card-footer">
               <p class="card-footer-item">
                 <span class="is-size-7">
                   «« _('Go back to') »»&thinsp;<a href="/">«« _('homepage') »»</a>
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
  },
  computed: {
    errorCode () {
      return Number(this.$route.params.code)
    }
  }
}
</script>
