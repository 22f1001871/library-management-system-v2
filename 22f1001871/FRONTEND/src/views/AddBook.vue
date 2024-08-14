<script setup>
import {ref } from 'vue';
import {useRouter} from 'vue-router';
import {messageStore} from '@/stores/messageStore';
import {auth} from '@/stores/auth'; 

const message_store = messageStore();
const auth_store = auth();

const router = useRouter();
const sections = ref([]);
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
                            message: 'Error Fetching Sections'
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

fetchSections();

const book_name = ref('');
const book_author = ref('');
const book_content = ref('');
const price = ref(0);
const sectionSelected = ref('');


function validate_input(){
    if (book_name==''){
        message_store.setmessage('Book Name is required');
        return false;
    }
    else if (book_author==''){
        message_store.setmessage('Author Name is required');
        return false;
    }
    else if (book_content==''){
        message_store.setmessage('Book Content is required');
        return false;
    }
    else if (price==0){
        message_store.setmessage('Book Price is required');
        return false;
    }
    return true
}
function addBook(){
    const book_details = {
        'name': book_name.value,
        'author': book_author.value,
        'content': book_content.value,
        'price': price.value,
        'section_name': sectionSelected.value
    }
    if (validate_input()){
        try{
            fetch(`${auth_store.backend_url}/api/v2/book`, {
                method: 'POST',
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
                                message: 'Error Adding Book'
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
    <h1 class="text-center">Add Book</h1>
    <div class="d-flex justify-content-center">
        <form class="w-50 justify-content-center" @submit.prevent="addBook">
            <div class="mb-3">
                <label for="book_name" class="form-label"><strong>Book Name</strong></label>
                <input type="text" class="form-control" id="book_name" v-model = 'book_name'>
            </div>
            <div class="mb-3 col-6">
                    <label for="book_author" class="form-label"><strong>Book Author</strong> </label>
                    <input type="text" class="form-control" id="book_author" v-model = 'book_author'>
                </div>
            <div class="mb-3">
                <label for="book_content" class="form-label"><strong>Book Content</strong></label>
                <textarea class="form-control" id="book_content" v-model = book_content></textarea>
            </div>
            <div class="row">
                <div class="mb-3 col-6">
                    <label for="price" class="form-label"><strong>Price</strong></label>
                    <input type="number" class="form-control" id="price" v-model = 'price' required>
                </div>
            </div>
            <div class="mb-3">
                <label for="section" class="form-label">Section</label>
                <select class="form-select" id="section" v-model="sectionSelected">
                    <option v-for="section in sections" :value="section.name" >{{ section.name }}</option>
                </select>
            </div>
            <div class="d-flex justify-content-center mb-3">
                <button type="submit" class="btn btn-primary">Add</button>
            </div>
        </form> 
    </div>
</div>
</template>