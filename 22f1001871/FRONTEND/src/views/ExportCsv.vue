<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';

const auth_store = auth();
const message_store = messageStore();
const router = useRouter();

const isLoading = ref(false); // Define isLoading as a reactive variable

async function exportcsv() {
    isLoading.value = true;
    try {
        const response = await fetch(`${auth_store.backend_url}/api/v2/exportcsv/${auth_store.email}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': auth_store.token
            },
        });

        if (!response.ok) {
            const errorData = await response.text();
            throw new Error(errorData || 'Error adding request');
        }

        // Check if the content type is JSON
        const contentType = response.headers.get('Content-Type');
        let data;

        if (contentType && contentType.includes('application/json')) {
            data = await response.json(); // Parse JSON if appropriate
        } else {
            const text = await response.text(); // Fallback to text parsing
            throw new Error(`Unexpected content type: ${contentType}. Response: ${text}`);
        }

        message_store.setmessage(data.message);
    } catch (error) {
        console.error('Export CSV error:', error);
        message_store.setmessage('An error occurred while exporting the CSV.');
    } finally {
        router.push('/downloaddashboard');
    }
}

// Call exportcsv when the component is mounted
exportcsv();
</script>

<template>
    <div>
        <p v-if="isLoading">Exporting CSV...</p>
        <p v-else>CSV export complete.</p>
    </div>
</template>