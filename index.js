import { createRouter, createWebHistory } from 'vue-router'  
  
const routes = [  
  { path: '/login', name: 'Login', component: () = },  
  { path: '/', redirect: '/dashboard' },  
  { path: '/dashboard', name: 'Dashboard', component: () = },  
  { path: '/devices', name: 'DeviceManage', component: () = },  
  { path: '/templates', name: 'TemplateList', component: () = },  
  { path: '/templates/edit/:id', name: 'TemplateEdit', component: () = },  
  { path: '/users', name: 'UserManage', component: () = },  
  { path: '/reports', name: 'ReportCenter', component: () = },  
]  
  
const router = createRouter({  
  history: createWebHistory(),  
  routes,  
})  
  
export default router 
