<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';

const auth_store = auth();
const message = ref('');
const router = useRouter();

async function downloadCSV() {
  try {
    const response = await fetch(`${auth_store.backend_url}/api/v2/get_file/${auth_store.email}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': auth_store.token,
      },
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    // Get the message from the response headers (if you want to display any)
    const messageHeader = response.headers.get('message');
    if (messageHeader) {
      message.value = messageHeader;
    }

    // Convert the response to a Blob
    const blob = await response.blob();

    // Handle the file download
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `report_${auth_store.email}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    router.push('/userdashboard')
  } catch (error) {
    console.error('Error downloading the CSV file', error);
    message.value = 'Error downloading the CSV file';
  }
}
</script>

<template>
  <div v-if="auth_store.isAuthenticated">
    <button @click="downloadCSV">Download CSV</button>
    <p v-if="message">{{ message }}</p>
  </div>
</template>