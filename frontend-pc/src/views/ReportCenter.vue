<template>
  <div class="page">
    <el-card>
      <template #header>
        <span>报表导出</span>
      </template>
      <el-form :model="form" label-width="100px">
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="form.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="设备筛选">
          <el-input v-model="form.deviceCode" placeholder="输入设备编号（可选）" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="exporting" @click="handleExport">
            {{ exporting ? '导出中...' : '导出 Excel' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const exporting = ref(false)
const form = reactive({
  dateRange: [],
  deviceCode: ''
})

const handleExport = async () => {
  if (!form.dateRange || form.dateRange.length !== 2) {
    ElMessage.warning('请选择日期范围')
    return
  }
  exporting.value = true
  try {
    const params = {
      start_date: form.dateRange[0],
      end_date: form.dateRange[1]
    }
    if (form.deviceCode) params.device_code = form.deviceCode

    const response = await axios.get('/api/v1/reports/export', {
      params,
      responseType: 'blob',
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `点检报表_${form.dateRange[0]}_${form.dateRange[1]}.xlsx`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (e) {
    ElMessage.error('导出失败')
  } finally {
    exporting.value = false
  }
}
</script>

<style scoped>
.page { padding: 20px; max-width: 600px; }
</style>