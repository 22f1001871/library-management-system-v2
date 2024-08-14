<script setup>
import { defineProps, ref } from 'vue';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { onMounted } from 'vue';
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';

const auth_store = auth();
const message_store = messageStore();
const router = useRouter();
const route = useRoute();

const book_id = route.params.id;

onMounted(() => {
  returnBook();
});

async function returnBook() {
  try {
    const response = await fetch(`${auth_store.backend_url}/api/v2/return/${book_id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': auth_store.token,
      },
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    message_store.setmessage(data.message);
    router.push('/userdashboard');
  } catch (error) {
    console.log(error);
    router.push('/userdashboard')
  }
}
</script>

<template>
  <div>
    Returning..
  </div>
</template>