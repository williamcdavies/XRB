import { createWebHistory, createRouter } from 'vue-router'

import LandingPage from './components/pages/landing'
import AboutPage from './components/pages/about'
import DashboardPage from './components/pages/dashboard'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/about', component: AboutPage },
  { path: '/dashboard', component: DashboardPage}
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router