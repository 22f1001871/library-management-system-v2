<script setup>
import { ref } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import statImage from '@/assets/stat.png';

const auth_store = auth();
const message_store = messageStore();
const route = useRoute();
const router = useRouter();

// Reactive variables
const imageSrc = ref(statImage);

// Function to fetch sections
async function fetchSections() {
  try {
    const response = await fetch(`${auth_store.backend_url}/api/v2/statistics`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': auth_store.token
      }
    });

    if (!response.ok) {
      const errorText = await response.text(); // Get error text
      console.error(`Fetch error: ${response.status} ${response.statusText} - ${errorText}`);
      throw new Error('Error showing statistics page');
    }

    const data = await response.json(); // Parse JSON response
    if (data.status === false) {
      message_store.setmessage(data.message);
    }

  } catch (error) {
    console.error('Fetch error:', error);
    message_store.setmessage('An error occurred while fetching statistics.');
  } 
}
</script>


<template>
  <nav class="navbar bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand h1 m-0" href="#">E-LIBRARY</a>
      <ul class="nav justify-content-end">
        <li class="nav-item" v-if="auth_store.isAuthenticated">
          <RouterLink class="nav-link" to="/librariandashboard">Home</RouterLink>
        </li>
      </ul>
    </div>
  </nav>
  <div>
    <img :src="imageSrc" alt="Statistics">
  </div>
  <div> 
    <button type="button" @click="fetchSections">Refresh</button>
  </div>
</template>