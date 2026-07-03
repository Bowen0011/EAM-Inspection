import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', name: 'Dashboard', component: () => import('../views/Dashboard.vue') },
  { path: '/devices', name: 'DeviceManage', component: () => import('../views/DeviceManage.vue') },
  { path: '/templates', name: 'TemplateList', component: () => import('../views/TemplateList.vue') },
  { path: '/templates/edit/:id', name: 'TemplateEdit', component: () => import('../views/TemplateEdit.vue') },
  { path: '/users', name: 'UserManage', component: () => import('../views/UserManage.vue') },
  { path: '/reports', name: 'ReportCenter', component: () => import('../views/ReportCenter.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
