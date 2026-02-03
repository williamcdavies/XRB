import { createWebHistory, createRouter } from 'vue-router'

import LandingPage from './components/pages/landing'
import AboutPage   from './components/pages/about'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/about', component: AboutPage}
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router