import { createWebHistory, createRouter } from 'vue-router';
import api from '../api'
import Login from '../views/Login.vue';
import Home from '../views/Home.vue';
import About from '../views/About.vue';

console.log('api logged in: ', api.isAuthenticated)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/about',
    name: 'About',
    component: About,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
