<script setup>
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { useRouter } from 'vue-router';

const message_store = messageStore();
const auth_store = auth();
const router = useRouter();

const logout = async () => {
  try {
    const response = await auth_store.logout();
    message_store.setmessage(response.message);
    router.push({ path: '/' });
  } catch (error) {
    console.error('Logout failed:', error);
  }
};

logout();
</script>

<template>
  <div>
    Logging Out......
    </div>
</template>