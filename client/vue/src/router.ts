// src/router.ts
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import Home from './Home.vue'
import XRB from './XRBTable.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/xrb',
    name: 'XRB',
    component: XRB
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router