<script setup>

import { onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';

// Store instances
const auth_store = auth();
const message_store = messageStore();

// Router and Route instances
const router = useRouter();
const route = useRoute();

const email = auth_store.email;

// Reactive object to hold book details
const book = ref({
    books : []
});

// Fetch book details from the backend
async function fetchcart() {
    try {
        const response = await fetch(`${auth_store.backend_url}/api/v2/view_request/${email}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Authentication-Token': auth_store.token
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch cart details');
        }

        const data = await response.json();
        book.value.books = data
    } catch (error) {
        console.error('Error fetching cart details:', error);
        message_store.setmessage('No Books available in Cart');
    }
}

// Execute fetchcart on component mount
onMounted(() => {
    fetchcart();
});

</script>

<template>
     <nav class="navbar bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand h1 m-0" href="#">E-LIBRARY</a>    
            <ul class="nav justify-content-end ">
                <li class="nav-item" v-if="auth_store.isAuthenticated">
                    <RouterLink class="nav-link" to="/userdashboard">Home</RouterLink>
                </li>
                <li class="nav-item" v-if="auth_store.isAuthenticated">
                    <RouterLink class="nav-link" to="/mybooks" >My Books</RouterLink>
                </li>
                <li class="nav-item" v-if="auth_store.isAuthenticated">
                    <RouterLink class="nav-link" to="/logout">Logout</RouterLink>
                </li>
                <li class="nav-item disabled" v-if="auth_store.isAuthenticated">
                    <a class="nav-link">{{auth_store.username}}</a>
                </li>
            </ul>
        </div>
    </nav>
    <div class="card col-3 m-1" v-for="books in book.books">
        <h5>Book Under Request</h5>
        <div class="card-body">
            <p class="card-title" >Book Name: {{ books.name }}</p>
            <p class="card-text">Date Requested: {{ books.date_requested }}</p>
            <p class="card-text">No Of Days Requested: {{ books.days_requested }}</p>
        </div>
    </div>
</template>

