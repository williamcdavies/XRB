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
    component: XRBPlot
  },
  {
    path: '/lrlxplot',
    name: 'LRLX Plot',
    component: LRLXPlot
  },
  {
    path: '/xrbtable',
    name: 'XRB Table',
    component: XRBTable
  },
  {
    path: '/lrlxtable',
    name: 'LRLX Table',
    component: LRLXTable
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router