<script setup>
import { RouterLink } from 'vue-router';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';


const auth_store = auth();
const all_users = ref([]);
const search_name = ref('');

onMounted(()=>{
  fetch_user();
})

function fetch_user(){
  try{
    fetch(`${auth_store.backend_url}/api/v2/login`, {
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
        all_users.value = data;
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
                    <RouterLink class="nav-link" to="/statistics">Statistics</RouterLink>
                </li>
                <li class="nav-item" v-if="auth_store.isAuthenticated && auth_store.role === 'admin'">
                    <RouterLink class="nav-link" to="/requests">Requests</RouterLink>
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
    <div class="card col-3 m-1" v-for="user in all_users" :key="user.id">
        <div class="card-body">
          <p class="card-text mt-4"><strong>User Id :</strong> {{user.user_id}}</p>
          <p class="card-text mt-4"><strong>User Name :</strong> {{user.name}}</p>
          <p class="card-text mt-4"><strong>User Email :</strong> {{user.email}}</p>
          <p class="card-text mt-4"><strong>Last Login :</strong> {{user.last_login_at}}</p>
          <p class="card-text mt-4"><strong>Login Count :</strong> {{user.login_count}}</p>
          </div>
    </div> 
</template>