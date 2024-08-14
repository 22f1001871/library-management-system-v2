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

// Reactive object to hold book details
const book = ref({
    books : []
});

// Fetch book details from the backend
async function fetchcart() {
    try {
        const response = await fetch(`${auth_store.backend_url}/api/v2/view_requests`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Authentication-Token': auth_store.token
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch Request details');
        }

        const data = await response.json();
        book.value.books = data
    } catch (error) {
        console.error('Error fetching Request details:', error);
        message_store.setmessage('Error fetching Request details');
    }
}

// Execute fetchcart on component mount
onMounted(() => {
    fetchcart();
});

function accept(bookid){
    try{
        fetch(`${auth_store.backend_url}/api/v2/approve_request/${bookid}`, {
            method: 'POST',
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

function reject(bookid){
    try{
        fetch(`${auth_store.backend_url}/api/v2/reject_request/${bookid}`, {
            method: 'POST',
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
</script>

<template>
    <nav class="navbar bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand h1 m-0" href="#">E-LIBRARY</a>
            <ul class="nav justify-content-end ">
                <li class="nav-item" v-if="auth_store.isAuthenticated && auth_store.role === 'admin'">
                    <RouterLink class="nav-link" to="/librariandashboard">Home</RouterLink>
                </li>
                <li class="nav-item" v-if="auth_store.isAuthenticated && auth_store.role === 'admin'">
                    <RouterLink class="nav-link" to="/statistics">Statistics</RouterLink>
                </li>
                <li class="nav-item" v-if="auth_store.isAuthenticated && auth_store.role === 'admin'">
                    <RouterLink class="nav-link" to="/users">Users Monitor</RouterLink>
                </li>
                <li class="nav-item" v-if="auth_store.isAuthenticated && auth_store.role === 'admin'">
                    <RouterLink class="nav-link" to="/approvedbooks">Book Issued</RouterLink>
                </li>
                <li class="nav-item" v-if="auth_store.isAuthenticated && auth_store.role === 'admin'">
                    <RouterLink class="nav-link" to="/add_book">Add Book</RouterLink>
                </li>
                <li class="nav-item" v-if="auth_store.isAuthenticated && auth_store.role !== 'user'">
                    <RouterLink class="nav-link" to="/add_section">Add Section</RouterLink>
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
        <h5>Request</h5>
        <div class="card-body">
            <p class="card-title" >Book Id: {{ books.request_id }}</p>
            <p class="card-text">User Id: {{ books.username }}</p>
        <div>
            <button class="btn btn-primary p-0 m-2" @click="() => accept(books.request_id)">Accept</button>
            <button class="btn btn-primary p-0 m-2" @click="() => reject(books.request_id)">Reject</button>
        </div>
        </div>
    </div>
</template>