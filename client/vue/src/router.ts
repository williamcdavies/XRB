// src/router.ts
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import Home from './Home.vue'
import XRBPlot from './XRBPlot.vue'
import LRLXPlot from './LRLXPlot.vue'
import XRBTable from './XRBTable.vue'
import LRLXTable from './LRLXTable.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/xrbplot',
    name: 'XRB Plot',
    component: XRBPlot,
    meta: { requiresAuth: true }
  },
  {
    path: '/lrlxplot',
    name: 'LRLX Plot',
    component: LRLXPlot,
    meta: { requiresAuth: true }
  },
  {
    path: '/xrbtable',
    name: 'XRB Table',
    component: XRBTable,
    meta: { requiresAuth: true }
  },
  {
    path: '/lrlxtable',
    name: 'LRLX Table',
    component: LRLXTable,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// authentication guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !token) {
    next('/')
  } else {
    next()
  }
})

export default router