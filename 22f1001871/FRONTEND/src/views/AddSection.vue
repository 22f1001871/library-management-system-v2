<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { messageStore } from '@/stores/messageStore';
import { auth } from '@/stores/auth';


const message_store = messageStore();
const auth_store = auth();
const router = useRouter();
const section = ref({
    name: '',
    description: ''
});

function validate_input(){
    if (section.name == ''){
        message_store.setmessage('Section Name is required');
        return false;
    }
    return true;
}

function addSection(){
    if (validate_input()){
        try{
            fetch(`${auth_store.backend_url}/api/v2/section`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Authentication-Token': auth_store.token
                    },
                body: JSON.stringify(section.value)
                }).then(
                    (response) =>{
                        if (!response.ok){
                            const resp = {
                                status: false,
                                message: 'Error Adding Section'
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
                            message_store.setmessage(data.message)
                        }
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
    <h1 class="text-center">Add Section</h1>
    <div class="d-flex justify-content-center">
        <form class="w-50 justify-content-center" @submit.prevent="addSection">
            <div class="mb-3">
                <label for="category_name" class="form-label">Section Name</label>
                <input type="test" class="form-control" id="category_name" v-model = section.name>
            </div>
            <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea class="form-control" id="description" v-model = 'section.description'></textarea>
            </div>
            <div class="d-flex justify-content-center mb-3">
                <button type="submit" class="btn btn-primary">Add</button>
            </div>
        </form>
    </div>  
</div>
</template>