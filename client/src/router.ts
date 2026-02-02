import { createWebHistory, createRouter } from 'vue-router'

import LandingPage from './components/pages/landing'

const routes = [
  { path: '/', component: LandingPage }
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router