<script setup>
import { defineProps, ref } from 'vue';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { onMounted } from 'vue';
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';

const route = useRoute();
const auth_store = auth();
const message_store = messageStore();
const router = useRouter();


const new_password = ref('');
const confirm_password = ref('');



function validate_input(){
    if (new_password==''){
        message_store.setmessage('New Password is required');
        return false;
    }
    return true
}

function editProfile(){
    const password_details = {
        'new_password': new_password.value,
        'confirm_password': confirm_password.value
    }
    if (validate_input()){
        try{
            fetch(`${auth_store.backend_url}/api/v2/editProfile/${auth_store.email}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Authentication-Token': auth_store.token
                    },
                body: JSON.stringify(password_details)
                }).then(
                    (response) =>{
                        if (!response.ok){
                            const resp = {
                                status: false,
                                message: 'Error updating Password'
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
                        router.push('/')
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
    <h1 class="text-center">Change Password</h1>
    <div class="d-flex justify-content-center">
        <form class="w-50 justify-content-center" @submit.prevent="editProfile">
            <div class="mb-3">
                <label for="author" class="form-label"><strong>New Password</strong></label>
                <textarea class="form-control" id="author" v-model = 'new_password' ></textarea>
            </div>
            <div class="mb-3">
                <label for="content" class="form-label"><strong>Confirm Password</strong></label>
                <textarea class="form-control" id="content" v-model = 'confirm_password' ></textarea>
            </div>
            <div class="d-flex justify-content-center mb-3">
                <button type="submit" class="btn btn-primary">Change Password</button>
            </div>
        </form> 
    </div>
</div>
</template>