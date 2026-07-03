<template>
  <div class="page">
    <div class="page-header">
      <el-select v-model="roleFilter" placeholder="角色筛选" clearable style="width:150px" @change="fetchUsers">
        <el-option label="技术员" value="tech" />
        <el-option label="工程师" value="engineer" />
        <el-option label="库管" value="store" />
      </el-select>
    </div>
    <el-table :data="users" stripe style="width:100%">
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column prop="real_name" label="真实姓名" width="120" />
      <el-table-column label="角色" width="100">
        <template #default="{ row }">
          <el-tag :type="row.role==='engineer'?'primary':row.role==='tech'?'success':'warning'" size="small">
            {{ {engineer:'工程师',tech:'技术员',store:'库管'}[row.role] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
            {{ row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="last_login_at" label="最近登录" width="180" />
      <el-table-column label="操作" min-width="200">
        <template #default="{ row }">
          <el-button type="warning" link size="small" @click="handleResetPwd(row)">重置密码</el-button>
          <el-button :type="row.is_active ? 'danger' : 'success'" link size="small"
            @click="handleToggleStatus(row)">
            {{ row.is_active ? '禁用' : '启用' }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/api/request.js'

const users = ref([])
const roleFilter = ref('')

const fetchUsers = async () => {
  try {
    const params = roleFilter.value ? { role: roleFilter.value } : {}
    users.value = await request.get('/users/list', { params })
  } catch (e) { ElMessage.error('加载用户列表失败') }
}

const handleResetPwd = async (row) => {
  try {
    await ElMessageBox.confirm(`确认将 ${row.real_name} 的密码重置为默认密码 123456？`)
    await request.post(`/users/${row.id}/reset-password`)
    ElMessage.success('密码已重置为 123456')
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('重置失败')
  }
}

const handleToggleStatus = async (row) => {
  const action = row.is_active ? '禁用' : '启用'
  try {
    await ElMessageBox.confirm(`确认${action}账号 ${row.real_name}？`)
    await request.put(`/users/${row.id}/toggle-status`, { is_active: !row.is_active })
    ElMessage.success(`账号已${action}`)
    fetchUsers()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('操作失败')
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.page { padding: 20px; }
.page-header { margin-bottom: 16px; }
</style>