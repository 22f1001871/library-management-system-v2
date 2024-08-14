<script setup>
/*
import { defineProps, ref } from 'vue';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { onMounted } from 'vue';
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import {useRoute } from 'vue-router';

const auth_store = auth();
const message_store = messageStore()
const router = useRouter();
const route = useRoute();

const book_id = route.params.id;

onMounted(()=>{
    deleteBook();
})


function deleteBook(){
    try{
        fetch(`${auth_store.backend_url}/api/v2/book/${book_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Authentication-Token':auth_store.token
            },
        }).then(
            (response) =>{
                return response.json();
            }
        ).then(
            (data)=>{
                message_store.setmessage(data.message);
                router.push('/librariandashboard')
            }
        )
    }
    catch(error){
        console.log(error);
    
    }
}
*/
import { onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';

// Store instances
const auth_store = auth();
const message_store = messageStore();

// Router and Route instances
const router = useRouter();
const route = useRoute();

// Extract book ID from route parameters
const book_id = route.params.id;

// Function to delete the book
async function deleteBook() {
    try {
        const response = await fetch(`${auth_store.backend_url}/api/v2/books/${book_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Authentication-Token': auth_store.token
            }
        });

        const data = await response.json();
        message_store.setmessage(data.message);
        router.push('/librariandashboard');
    } catch (error) {
        console.log(error);
    }
}

// Execute deleteBook on component mount
onMounted(() => {
    deleteBook();
});

</script>

<template>
    <div>
      Deleting book...
    </div>
  </template>