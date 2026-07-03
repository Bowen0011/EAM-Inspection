<template>
  <router-view v-if="$route.path === '/login'" />
  <el-container v-else style="height: 100vh">
    <el-aside width="220px" style="background-color: #304156">
      <el-menu :default-active="$route.path" router background-color="#304156" text-color="#bfcbd9" active-text-color="#409EFF" style="border-right: none">
        <el-menu-item index="/dashboard"><el-icon><Monitor /></el-icon><span>Dashboard</span></el-menu-item>
        <el-menu-item index="/devices"><el-icon><Tools /></el-icon><span>Device Management</span></el-menu-item>
        <el-menu-item index="/templates"><el-icon><Document /></el-icon><span>Inspection Templates</span></el-menu-item>
        <el-menu-item index="/users"><el-icon><User /></el-icon><span>User Management</span></el-menu-item>
        <el-menu-item index="/reports"><el-icon><DataAnalysis /></el-icon><span>Report Center</span></el-menu-item>
      </el-menu>
    </el-aside>
    <el-main style="padding: 20px; background-color: #f0f2f5"><router-view /></el-main>
  </el-container>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { Monitor, Tools, Document, User, DataAnalysis } from '@element-plus/icons-vue'
const route = useRoute()
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, #app { height: 100%; }
</style>
