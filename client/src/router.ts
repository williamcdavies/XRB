import { createWebHistory, createRouter } from 'vue-router'

import Landing from './components/landing/Landing.vue'

const routes = [
  { path: '/', component: Landing }
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router