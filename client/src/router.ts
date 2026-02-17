import { createWebHistory, createRouter } from 'vue-router'
import { useAuth }                        from './composables/auth'

import AboutPage                          from './components/pages/about'
import LandingPage                        from './components/pages/landing'
import DashboardPage                      from './components/pages/dashboard'
import DocumentPage                       from './components/pages/document'


const routes = [
  { path: '/',          component: LandingPage },
  { path: '/about',     component: AboutPage },
  { path: '/dashboard', component: DashboardPage, meta: { requiresAuth: false }},
  { path: '/document',  component: DocumentPage,  meta: { requiresAuth: false }},
]


export const router = createRouter({
  history: createWebHistory(),
  routes,
})


router.beforeEach(async (to) => {
  const { isAuthenticated } = useAuth()

  if(!to.meta.requiresAuth) {
    return
  }

  if(await isAuthenticated()) {
    return
  } 

  return '/'
})


export default router