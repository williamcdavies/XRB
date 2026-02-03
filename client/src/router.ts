import { createWebHistory, createRouter } from 'vue-router'

import AboutPage   from './components/pages/about'
import LandingPage from './components/pages/landing'


const routes = [
  { path: '/', component: LandingPage },
  { path: '/about', component: AboutPage}
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router