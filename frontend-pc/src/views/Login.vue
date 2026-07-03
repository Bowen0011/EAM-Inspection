<template>
  <div class="login-container">
    <el-card class="login-card" shadow="always">
      <h2 class="login-title">EAM 点检管理系统</h2>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="0" size="large"
        @keyup.enter="handleLogin">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码"
            prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" style="width:100%" @click="handleLogin">
            登 录
          </el-button>
        </el-form-item>
      </el-form>
      <div class="version-text">V1.0</div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '@/api/request.js'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({ username: 'admin', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    const res = await request.post('/auth/login', form)
    localStorage.setItem('token', res.access_token)
    localStorage.setItem('userInfo', JSON.stringify(res))
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1a73e8 0%, #1557b0 100%);
}
.login-card { width: 420px; padding: 20px; }
.login-title { text-align: center; color: #1a73e8; margin-bottom: 30px; font-size: 24px; }
.version-text { text-align: center; color: #999; font-size: 12px; margin-top: 10px; }
</style>