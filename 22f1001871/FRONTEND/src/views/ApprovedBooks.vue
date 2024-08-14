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

const his = ref({
    books : []
});

// Fetch book details from the backend
async function fetchcart() {
    try {
        const response = await fetch(`${auth_store.backend_url}/api/v2/approvedbooks`, {
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
        message_store.setmessage('No approved books');
    }
}

// Fetch book details from the backend
async function fetchhistory() {
    try {
        const response = await fetch(`${auth_store.backend_url}/api/v2/history`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Authentication-Token': auth_store.token
            }
        });

        if (!response.ok) {
            throw new Error('No History details');
        }

        const data = await response.json();
        his.value.books = data
    } catch (error) {
        message_store.setmessage('No approved books');
    }
}


// Execute fetchcart on component mount
onMounted(() => {
    fetchcart();
    fetchhistory();
});


function revoke(bookid){
    try{
        fetch(`${auth_store.backend_url}/api/v2/return/${bookid}`, {
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
    <h5>Books Issued</h5>
    <div class="card col-3 m-1" v-for="books in book.books">
        <div class="card-body">
            <p class="card-title" >Book Id: {{ books.request_id }}</p>
            <p class="card-text">Book Name: {{ books.name }}</p>
            <p class="card-text">Date Accessed: {{ books.date_requested }}</p>
            <p class="card-text">Returning Date: {{ books.date_returning }}</p>
        <div>
            <button class="btn btn-primary p-0 m-2" @click="() => revoke(books.book_id)">Revoke</button>
        </div>
        </div>
    </div>
    <h5>History of Book returned</h5>
    <div class="card col-3 m-1" v-for="books in his.books">
        <div class="card-body">
            <p class="card-title" >Book Id: {{ books.book_id }}</p>
            <p class="card-text">User Id: {{ books.user_id }}</p>
            <p class="card-text">Description: {{ books.description }}</p>
            <p class="card-text">Date Requested: {{ books.date_requested }}</p>
            <p class="card-text">Date Accessed: {{ books.days_requested }}</p>
            <p class="card-text">Date Returned: {{ books.date_returned }}</p>
        </div>
    </div>
</template>