<template>
 <div class="hero is-fullheight">
   <div class="hero-body">
     <div class="container">
       <div class="columns is-centered">
         <div class="column is-one-third">
           <div class="box">
             <h1 class="title">«« _('Log in') »»</h1>
             <login-form></login-form>
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
