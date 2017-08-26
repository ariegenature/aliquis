<template>
 <div class="hero is-fullheight">
   <div class="hero-body">
     <div class="container">
       <div class="columns is-centered">
         <div class="column is-two-third">
           <div class="box">
             <h1 class="title">«« _('Create Your ANA Account') »»</h1>
             <sign-up-form></sign-up-form>
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
