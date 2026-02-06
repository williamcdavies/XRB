import { createWebHistory, createRouter } from 'vue-router'

import LandingPage from './components/pages/landing'
import AboutPage from './components/pages/about'
import DocumentPage from './components/pages/document'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/about', component: AboutPage },
  { path: '/document', component: DocumentPage },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router