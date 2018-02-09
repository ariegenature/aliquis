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
               <reset-form></reset-form>
             </div>
           </div>
         </div>
       </div>
     </div>
   </div>
 </div>
</template>

<script>
import ResetForm from './ResetForm'

export default {
  name: 'reset-page',
  components: {
    ResetForm
  }
}
</script>
