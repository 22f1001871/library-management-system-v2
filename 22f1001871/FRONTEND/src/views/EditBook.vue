<script setup>
import { defineProps, ref } from 'vue';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { onMounted } from 'vue';
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';

const route = useRoute();
const book_id = route.params.id;
const auth_store = auth();
const message_store = messageStore();
const router = useRouter();
onMounted(()=>{
    fetchBook();
    fetchSections();
})

const sectionSelected= ref('');
const sections = ref({});
const book = ref([]);
function fetchSections(){
    try{
        fetch(`${auth_store.backend_url}/api/v2/get_all_sections`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                },
            }).then(
                (response) =>{
                    if (!response.ok){
                        const resp = {
                            status: false,
                            message: 'Error Fetching Categories'
                        }
                        return resp
                    }
                    else{
                        return response.json();
                    }
                }
            ).then(
                (data)=>{
                    if (data.status == false){
                        message_store.setmessage(data.message)
                    }
                    else{
                        sections.value = data;
                    }
                }
            )
    }
    catch(error){
        console.log(error);
    }
}

function fetchBook(){
    try{
        fetch(`${auth_store.backend_url}/api/v2/book/${book_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                },
            }).then(
                (response) =>{
                    return response.json();
                }
            ).then(
                (data)=>{
                    book.value = data;
                    sectionSelected.value = data.section_name;
                }
            )
    }
    catch(error){
        console.log(error);
    }
}

function validate_input(){
    if (book.name==''){
        message_store.setmessage('Book Name is required');
        return false;
    }
    if (book.author==''){
        message_store.setmessage('Author Name is required');
        return false;
    }
    if (book.content==''){
        message_store.setmessage('Book Content is required');
        return false;
    }
    if (price==0){
        message_store.setmessage('Book Price is required');
        return false;
    }
    return true
}

function editBook(){
    const book_details = {
        'name': book.value.name,
        'author': book.value.author,
        'content':book.value.content,
        'price': book.value.price,
        'section': sectionSelected.value
    }
    if (validate_input()){
        try{
            fetch(`${auth_store.backend_url}/api/v2/books/${book_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Authentication-Token': auth_store.token
                    },
                body: JSON.stringify(book_details)
                }).then(
                    (response) =>{
                        if (!response.ok){
                            const resp = {
                                status: false,
                                message: 'Error updating Book'
                            }
                            return resp
                        }
                        else{
                            return response.json();
                        }
                    }
                ).then(
                    (data)=>{
                        message_store.setmessage(data.message)
                        router.push('/librariandashboard')
                    }
                )
        }
        catch(error){
            console.log(error);
        }

    }
}

</script>

<template>
<div class="container-fluid mt-2 p-3">
    <h1 class="text-center">Edit Book Details</h1>
    <div class="d-flex justify-content-center">
        <form class="w-50 justify-content-center" @submit.prevent="editBook">
            <div class="mb-3">
                <label for="book_name" class="form-label"><strong>Book Name</strong></label>
                <input type="text" class="form-control" id="book_name" v-model = "book.name">
            </div>
            <div class="mb-3">
                <label for="author" class="form-label"><strong>Author</strong></label>
                <textarea class="form-control" id="author" v-model = 'book.author' ></textarea>
            </div>
            <div class="mb-3">
                <label for="content" class="form-label"><strong>Content</strong></label>
                <textarea class="form-control" id="content" v-model = 'book.content' ></textarea>
            </div>
            <div class="row">
                <div class="mb-3 col-6">
                    <label for="price" class="form-label"><strong>Price</strong></label>
                    <input type="number" class="form-control" id="price" v-model="book.price" required>
                </div>
            </div>
            <div class="mb-3">
                <label for="section" class="form-label">Section</label>
                <select class="form-select" id="category" v-model="sectionSelected">
                    <option v-for="section in sections":value="section.name">{{ section.name }}</option>
                </select>
            </div>
            <div class="d-flex justify-content-center mb-3">
                <button type="submit" class="btn btn-primary">Edit Product</button>
            </div>
        </form> 
    </div>
</div>

</template>