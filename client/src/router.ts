import { createWebHistory, createRouter } from 'vue-router'

import Landing from './components/landing/Hero.vue'

const routes = [
  { path: '/', component: Landing }
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router