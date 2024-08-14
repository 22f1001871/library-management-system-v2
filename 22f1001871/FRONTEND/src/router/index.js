import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/userlogin',
      name: 'userlogin',
      component: () => import('../views/UserLogin.vue')
    },
    {
      path: '/librarianlogin',
      name: 'librarianlogin',
      component: () => import('../views/LibrarianLogin.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue')
    },
    {
      path: '/userdashboard',
      name: 'userdashboard',
      component: () => import('../views/UserDashboard.vue')
    },
    {
      path: '/logout',
      name: 'logout',
      component: () => import('../views/Logout.vue')
    },
    {
      path: '/librariandashboard',
      name: 'librariandashboard',
      component: () => import('../views/LibrarianDashboard.vue')
    },
    {
      path:'/add_book',
      name: 'add_book',
      component: () => import('../views/AddBook.vue')
    },
    {
      path:'/add_section',
      name: 'add_section',
      component: () => import('../views/AddSection.vue')
    },
    {
      path:'/delete_book/:id',
      name: 'delete_book',
      component: () => import('../views/DeleteBook.vue')
    },
    {
      path:'/edit_book/:id',
      name: 'edit_book',
      component: () => import('../views/EditBook.vue')
    },
    {
      path:'/delete_section/:id',
      name: 'delete_section',
      component: () => import('../views/DeleteSection.vue')
    },
    {
      path:'/edit_section/:id',
      name: 'edit_section',
      component: () => import('../views/EditSection.vue')
    },
    {
      path:'/mybooks',
      name: 'mybooks',
      component: () => import('../views/MyBook.vue')
    },
    {
      path:'/addrat/:id/Rating/:rate',
      name: 'search',
      component: () => import('../views/Addrat.vue')
    },
    {
      path:'/requests',
      name: 'requests',
      component: () => import('../views/Requests.vue')
    },
    {
      path:'/return/:id',
      name: 'return',
      component: () => import('../views/Return.vue')
    },
    {
      path:'/mycart',
      name: 'mycart',
      component: () => import('../views/MyCart.vue')
    },
    {
      path:'/addreq/:id/Days/:day',
      name: 'add_req',
      component: () => import('../views/AddRequests.vue')
    },
    {
      path:'/approvedbooks',
      name: 'approvedBooks',
      component: () => import('../views/ApprovedBooks.vue')
    },
    {
      path:'/statistics',
      name: 'statistics',
      component: () => import('../views/Statistics.vue')
    },
    {
      path:'/users',
      name: 'user_monitor',
      component: () => import('../views/Users.vue')
    },
    {
      path:'/exportcsv',
      name: 'csv_export',
      component: () => import('../views/ExportCsv.vue')
    },
    {
      path:'/editProfile',
      name: 'csv export',
      component: () => import('../views/EditProfile.vue')
    },
    {
      path:'/downloaddashboard',
      name: 'csv download',
      component: () => import('../views/Downloadcsv.vue')
    }
  ]
})

export default router
