<template>
  <div class="page">
    <el-card class="construction-card">
      <div class="construction-content">
        <el-icon class="construction-icon" :size="64" color="#909399">
          <Tools />
        </el-icon>
        <h2>功能开发中</h2>
        <p>设备管理功能正在开发中，敬请期待</p>
        <p class="hint">预计下一版本上线</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { Tools } from '@element-plus/icons-vue'
</script>

<style scoped>
.page { padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 60vh; }
.construction-card { width: 500px; }
.construction-content { text-align: center; padding: 40px 0; }
.construction-icon { margin-bottom: 20px; }
h2 { color: #606266; margin-bottom: 8px; }
p { color: #909399; font-size: 14px; }
.hint { margin-top: 12px; font-size: 12px; color: #c0c4cc; }
</style>