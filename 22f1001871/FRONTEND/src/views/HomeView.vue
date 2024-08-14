<script setup>
import { RouterLink } from 'vue-router';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
</script>

<template>
  <main>
    <h1 class="text-center">WELCOME TO E-LIBRARY</h1>
    <div class="d-flex justify-content-center">
    <RouterLink class="btn btn-primary justify-content-center" to="/userlogin" >LOGIN/REGISTER </RouterLink>
    </div>
    <h2 class="text-center">CLICK HERE TO LOGIN/REGISTER</h2>
    <div class="d-flex justify-content-center">
    <RouterLink class="btn btn-primary justify-content-center" to="/librarianlogin" >LIBRARIAN LOGIN</RouterLink>
    </div>
  </main>
</template>

