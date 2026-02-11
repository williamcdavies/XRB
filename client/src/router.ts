import { createWebHistory, createRouter } from 'vue-router'
import { useAuth }                        from './composables/auth'

import AboutPage                          from './components/pages/about'
import LandingPage                        from './components/pages/landing'
import DashboardPage                      from './components/pages/dashboard'


const routes = [
  { path: '/',          component: LandingPage },
  { path: '/about',     component: AboutPage },
  { path: '/dashboard', component: DashboardPage, meta: { requiresAuth: true }},
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