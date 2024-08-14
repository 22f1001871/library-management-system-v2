<script setup>
import { onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';

// Store instances
const auth_store = auth();
const message_store = messageStore();

// Router and Route instances
const router = useRouter();
const route = useRoute();

// Extract book ID from route parameters
const book_id = route.params.id;
const rating = route.params.rate;
const user_email = auth_store.email;

function validate_input(){
    if (rating===0){
        message_store.setmessage('Days is required');
        return false;
    }
    return true
}

function addrate(){
    const book_details = {
        'book_id': book_id,
        'email': user_email,
        'rating': rating
    }
    if (validate_input()){
        try{
            fetch(`${auth_store.backend_url}/api/v2/rate`, {
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
                                message: 'Error Adding Request'
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
                        router.push('/userdashboard')
                    }
                )
        }
        catch(error){
            console.log(error);
        }

    }
}

// Execute deleteBook on component mount
onMounted(() => {
    addrate();
});

</script>

<template>
    <div>
    Rating...
    </div>
</template>