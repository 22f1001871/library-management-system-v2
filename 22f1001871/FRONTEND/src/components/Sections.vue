<script setup>
import { ref } from 'vue';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { onMounted } from 'vue';
import {computed} from 'vue';
import Books from '@/components/Books.vue';

const auth_store = auth();
const message_store = messageStore()
const section = defineProps(['section_id']);
const section_data = ref({
    section_id: 0,
    section_name: '',
    description: '',
    books: []
});


const search_name = ref('');

onMounted(()=>{
    getSection(section.section_id);
    getBooks(section.section_id);
})


function getSection(section_id) {
    try{
        fetch(`${auth_store.backend_url}/api/v2/section/${section.section_id}`, {
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
                    section_data.value.section_id = data.id;
                    section_data.value.section_name = data.name;
                    section_data.value.description = data.description;
                }
            )
    }
    catch(error){
        console.log(error);
    }
}

function getBooks(section_id) {
    try{
        fetch(`${auth_store.backend_url}/api/v2/section/${section_id}/books`, {
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
                    section_data.value.books = data
                }
            )
    }
    catch(error){
        console.log(error);
    }
}

const update_url = computed(()=>`/edit_section/${section_data.value.section_id}`);
const delete_url = computed(()=>`/delete_section/${section_data.value.section_id}`);

function search(){
  try{
    fetch(`${auth_store.backend_url}/api/v2/search_book/${search_name.value}/${section_data.value.section_id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    }).then(
      (response) => {
        if (!response.ok){
          const data =  response.json()
          const rsp = {
              'status': false,
              'message': data.message
          }
          return rsp
        }
        else {
          return response.json()
        }
      }
    ).then(
      (data) => {
        if (data.status === false){
          messageStore.addMessage(data.message, 'danger')
          return
        }
        section_data.value.books = data
      }
    )
  }
  catch(error){
    console.log(error);
  }
}

</script>

<template>
    <div class="container-fluid mt-1 p-2">
    <div class="row">
        <div class="col-8">
            <p class="h1">{{section_data.section_name}}</p>
            <p>{{section_data.description}}</p>
        </div>
        <div class="col-4 d-flex justify-content-end" v-if="auth_store.isAuthenticated && auth_store.role === 'admin'">
            <RouterLink class="btn btn-primary p-1 m-5" :to="update_url" >Update</RouterLink>
            <RouterLink class="btn btn-primary p-1 m-5" :to="delete_url" >Delete</RouterLink>
        </div>
    </div>
    <div class="row">
        <p>search_based_on_book/author</p>
        <form class="d-flex" role="search" @submit.prevent="search">
          <input type="text" class="form-control" id="search_name" v-model = 'search_name'>
          <button class="btn btn-outline-success" type="submit" >Search</button>
         </form>
      <h5>Books</h5>
        <Books v-for="book in section_data.books" :book_details="book" :key="book.book_id"/>
    </div>  
</div>
</template>