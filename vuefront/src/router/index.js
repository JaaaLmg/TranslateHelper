import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'homepage',
    component: () => import('../views/translate/HomePage.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/translate/LoginPage.vue')
  },
  {
    path:'/upload',
    name:'upload',
    component: () => import('../views/translate/UploadPage.vue')
  },
  {
    path:'/project',
    name:'project',
    component: () => import('../views/translate/CreateProject.vue')
  },
  {
    path:'/translate',
    name:'translate',
    component: () => import('../views/translate/TranslatePage.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
