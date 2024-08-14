<script setup>
import { RouterLink } from 'vue-router';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';
import { computed } from 'vue';
import Sec from '../components/Sections.vue'


const auth_store = auth();
const message_store = messageStore();
const router = useRouter();

const all_sections = ref([]);
onMounted(()=>{
  fetch_sections();
})

const search_name=ref('');

function fetch_sections(){
  try{
    fetch(`${auth_store.backend_url}/api/v2/get_all_sections`, {
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
        all_sections.value = data;
      }
    )
  }
  catch(error){
    console.log(error);
  }
}

function search(){
  try{
    fetch(`${auth_store.backend_url}/api/v2/search_section/${search_name.value}`, {
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
        all_sections.value = data;
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
        
            <form class="d-flex" role="search" @submit.prevent="search">
                <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model = 'search_name'>
                <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
    
            <ul class="nav justify-content-end ">
                <li class="nav-item" v-if="auth_store.isAuthenticated">
                  <RouterLink class="nav-link" to="/exportcsv">Export as CSV</RouterLink>
                </li>
                <li class="nav-item" v-if="auth_store.isAuthenticated && auth_store.role === 'admin'">
                    <RouterLink class="nav-link" to="/add_book">Add Book</RouterLink>
                </li>
                <li class="nav-item" v-if="auth_store.isAuthenticated && auth_store.role === 'user'">
                    <RouterLink class="nav-link" to="/mycart">Cart</RouterLink>
                </li>
                <li class="nav-item" v-if="auth_store.isAuthenticated && auth_store.role === 'user'">
                    <RouterLink class="nav-link" to= "/mybooks" >My Books</RouterLink>
                </li>
                <li class="nav-item" v-if="auth_store.isAuthenticated && auth_store.role !== 'user'">
                    <RouterLink class="nav-link" to="/add_section">Add Section</RouterLink>
                </li>
                <li class="nav-item" v-if="auth_store.isAuthenticated">
                    <RouterLink class="nav-link" to="/logout">Logout</RouterLink>
                </li>
                <li class="nav-item disabled" v-if="auth_store.isAuthenticated">
                    <RouterLink class="nav-link" to="/editProfile">{{auth_store.username}}</RouterLink>
                </li>
            </ul>
        </div>
      </nav>
      <Sec v-for="section in all_sections" :section_id="section.id" :key="section.id"/>
</template>