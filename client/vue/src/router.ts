// src/router.ts
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import Home from './Home.vue'
import XRBTable from './XRBTable.vue'
import XRBPlot from './XRBPlot.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/xrbtable',
    name: 'XRB Table',
    component: XRBTable
  },
  {
    path: '/xrbplot',
    name: 'XRB Plot',
    component: XRBPlot
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router