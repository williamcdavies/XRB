import { createWebHistory, createRouter } from 'vue-router'

import DashboardPage from './components/pages/dashboard'
import LandingPage from './components/pages/landing'
import DocumentPage from './components/pages/document'

const routes = [
  { path: '/', component: LandingPage }
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router