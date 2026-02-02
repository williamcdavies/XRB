import { createWebHistory, createRouter } from 'vue-router'

import DashboardPage from './components/pages/dashboard'
import LandingPage from './components/pages/landing'

const routes = [
  { path: '/', component: DashboardPage }
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router