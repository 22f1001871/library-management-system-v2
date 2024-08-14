<script setup>
import {useRoute} from 'vue-router';
import {auth} from '@/stores/auth';
import {messageStore} from '@/stores/messageStore';
import {onMounted} from 'vue';
import {computed} from 'vue';
import {useRouter} from 'vue-router';
import { ref } from 'vue';

const auth_store = auth();
const message_store = messageStore();
const route = useRoute();  
const router = useRouter();
const section_id = route.params.id;

const section = ref({
    name: '',
    description: ''
});

onMounted(()=>{
    getSection();
})

function getSection(){
    try{
        fetch(`${auth_store.backend_url}/api/v2/section/${section_id}`, {
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
                    section.value.name = data.name;
                    section.value.description = data.description;
                }
            )
    }
    catch(error){
        console.log(error);
    }
}


function validate_input(){
    if (section.value.section_name == ''){
        message_store.setmessage('Section Name is required');
        return false;
    }
    return true;
}

function editSection(){
    if (validate_input()){
        try{
            fetch(`${auth_store.backend_url}/api/v2/section/${section_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Authentication-Token': auth_store.token
                    },
                body: JSON.stringify(section.value)
                }).then(
                    (response) =>{
                        return response.json();
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
        <h1 class="text-center">Edit Section</h1>
        <div class="d-flex justify-content-center">
            <form class="w-50 justify-content-center" @submit.prevent="editSection">
                <div class="mb-3">
                    <label for="section_name" class="form-label">Section Name</label>
                    <input type="test" class="form-control" id="section_name" v-model = section.name>
                </div>
                <div class="mb-3">
                    <label for="description" class="form-label">Description</label>
                    <textarea class="form-control" id="description" v-model = 'section.description'></textarea>
                </div>
                <div class="d-flex justify-content-center mb-3">
                    <button type="submit" class="btn btn-primary">Edit</button>
                </div>
            </form>
        </div>  
    </div>
</template>
    