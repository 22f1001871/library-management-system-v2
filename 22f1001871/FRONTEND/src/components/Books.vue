<script setup>
import { ref } from 'vue';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { onMounted } from 'vue';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const auth_store = auth();
const message_store = messageStore()
const router = useRouter();
const books = defineProps(['book_details']);
const Days = ref(0);
const Rating = ref(0);
const update_url = computed(() => {
    return `/edit_book/${books.book_details.book_id}`
})
const delete_url = computed(() => {
    return `/delete_book/${books.book_details.book_id}`
})
const add_req = computed(() => {
    return `/addreq/${books.book_details.book_id}/Days/${Days.value}`
})
const add_rating = computed(() => {
    return `/addrat/${books.book_details.book_id}/rating/${Rating.value}`
})

const downloadPdf = () => {
  // URL of the PDF file
  const pdfUrl = 'Thirukural.pdf';

  // Create an anchor element and set the href attribute to the PDF URL
  const link = document.createElement('a');
  link.href = pdfUrl;

  // Set the download attribute to suggest a default file name
  link.download = 'example.pdf';

  // Append the anchor element to the document body
  document.body.appendChild(link);

  // Programmatically click the anchor element to trigger the download
  link.click();

  // Remove the anchor element from the document body
  document.body.removeChild(link);
};

</script>

<template>
  <div class="card col-3 m-1">
        <div class="card-body">
            <h5 class="card-title">{{books.book_details.name}}</h5>
            <p class="card-text"><em>{{books.book_details.author}}</em></p>
            <div class="row">
                <div class="col-6">
                    <p class="card-text mt-4"><strong>Price:</strong> {{books.book_details.price}}</p>
                </div>
            </div>
            <div class="row mt-3 container-fluid justify-content-center" v-if="auth_store.isAuthenticated && auth_store.role==='user'">
                <form class="w-50 justify-content-center">
                    <div class="mb-3 col-6">
                        <label for="price" class="form-label"><strong>Provide rating</strong></label>
                        <input type="number" class="form-control" id="Days.value" v-model="Rating" required>
                    </div>
                    <div class="d-flex justify-content-center mb-3">
                        <RouterLink class="btn btn-primary" :to="add_rating" >Rate</RouterLink>
                    </div>
                </form>
            </div>
            <div class="row mt-3 container-fluid justify-content-center" v-if="auth_store.isAuthenticated && auth_store.role==='admin'">
                <div class="col-6">
                    <RouterLink class="btn btn-primary" :to="update_url" >Edit</RouterLink>
                </div>
                <div class="col-6">
                    <RouterLink class="btn btn-primary" :to="delete_url" >Delete</RouterLink>
                </div>
            </div>
            <div class="row mt-3 container-fluid justify-content-center" v-if="auth_store.isAuthenticated && auth_store.role==='user' && books.book_details.user_id===0">
                <form class="w-50 justify-content-center">
                    <div class="mb-3 col-6">
                        <label for="price" class="form-label"><strong>Number of days Book required</strong></label>
                        <input type="number" class="form-control" id="Days.value" v-model="Days" required>
                    </div>
                    <div class="d-flex justify-content-center mb-3">
                        <RouterLink class="btn btn-primary" :to="add_req" >Request</RouterLink>
                    </div>
                </form>
                </div>
            </div>
            <div class="row mt-3 container-fluid justify-content-center" v-if="auth_store.isAuthenticated && auth_store.role==='user' && books.book_details.user_id!==0">
                <div class="col-6">
                    <p class="card-text mt-4"><strong>User Issued/Requested:</strong> {{books.book_details.user_id}}</p>
                </div>
                <div class="col-6">
                    <p class="card-text mt-4"><strong>Returning Date:</strong> {{books.book_details.return_date}}</p>
                </div>
            </div>
            <div class="d-flex justify-content-center mb-3" v-if="auth_store.isAuthenticated && auth_store.role==='user'">
            <div>
                <button @click="downloadPdf">Download PDF</button>
            </div>
        </div>
    </div> 
</template> 