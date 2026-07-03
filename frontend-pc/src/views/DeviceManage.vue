<template>
  <div class="page">
    <div class="page-header">
      <el-button type="primary" @click="openCreate">新增设备</el-button>
      <el-upload
        action="/api/v1/devices/import"
        :headers="{ Authorization: `Bearer ${token}` }"
        :on-success="onImportSuccess"
        :on-error="onImportError"
        accept=".xlsx,.xls"
        :show-file-list="false"
        style="display:inline-block;margin-left:8px"
      >
        <el-button type="success">批量导入</el-button>
      </el-upload>
    </div>

    <el-table :data="devices" stripe style="width:100%">
      <el-table-column prop="device_code" label="设备编号" width="220" />
      <el-table-column prop="device_name" label="设备名称" width="180" />
      <el-table-column label="线别" width="80">
        <template #default="{ row }">{{ row.device_code?.split('-')[1] }}</template>
      </el-table-column>
      <el-table-column label="站别" width="100">
        <template #default="{ row }">{{ row.device_code?.split('-')[2] }}</template>
      </el-table-column>
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_deleted ? 'danger' : 'success'" size="small">
            {{ row.is_deleted ? '已退役' : '正常' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="location" label="位置" min-width="200" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button v-if="!row.is_deleted" type="warning" size="small"
            @click="retireDevice(row)">退役</el-button>
          <el-button v-else type="success" size="small"
            @click="activateDevice(row)">启用</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialog.visible" title="新增设备" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="线别" required>
          <el-select v-model="form.line" placeholder="请选择线别" style="width:100%">
            <el-option v-for="item in codeRules.line_options" :key="item" :value="item" :label="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="站别" required>
          <el-select v-model="form.station" placeholder="请选择站别" style="width:100%">
            <el-option v-for="item in codeRules.station_options" :key="item" :value="item" :label="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="设备号" required>
          <el-input v-model="form.deviceNo" placeholder="01-99" maxlength="2" />
        </el-form-item>
        <el-form-item label="设备名称" required>
          <el-input v-model="form.deviceName" placeholder="请输入设备名称" />
        </el-form-item>
        <el-form-item label="编码预览">
          <el-tag type="info">{{ codePreview }}</el-tag>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog.visible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="submitDevice">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/api/request.js'

const devices = ref([])
const codeRules = reactive({ line_options: [], station_options: [] })
const token = localStorage.getItem('token') || ''
const saving = ref(false)

const dialog = reactive({ visible: false })
const form = reactive({ line: '', station: '', deviceNo: '', deviceName: '' })

const codePreview = computed(() => {
  if (form.line && form.station && form.deviceNo) {
    return `CSGZ-${form.line}-${form.station}-${String(form.deviceNo).padStart(2, '0')}`
  }
  return '请完整填写以上信息'
})

const fetchDevices = async () => {
  try { devices.value = (await request.get('/devices/list')).devices || [] }
  catch (e) { ElMessage.error('加载设备列表失败') }
}

const fetchCodeRules = async () => {
  try {
    const rules = await request.get('/devices/code-rules')
    Object.assign(codeRules, rules)
  } catch (e) { console.error('加载编码规则失败', e) }
}

const openCreate = () => {
  form.line = ''; form.station = ''; form.deviceNo = ''; form.deviceName = ''
  dialog.visible = true
}

const submitDevice = async () => {
  if (!form.line || !form.station || !form.deviceNo || !form.deviceName) {
    ElMessage.warning('请完整填写所有字段')
    return
  }
  saving.value = true
  try {
    const deviceCode = codePreview.value
    await request.put(`/devices/${encodeURIComponent(deviceCode)}/activate`, {
      device_code: deviceCode, device_name: form.deviceName,
      location: `${form.line}线-${form.station}`, template_id: 1
    })
    ElMessage.success('设备已创建')
    dialog.visible = false
    fetchDevices()
  } catch (e) { ElMessage.error(e.response?.data?.detail || '创建失败') }
  finally { saving.value = false }
}

const retireDevice = async (row) => {
  try {
    await ElMessageBox.confirm(`确认将设备 ${row.device_code} 退役？`)
    await request.put(`/devices/${encodeURIComponent(row.device_code)}/retire`)
    ElMessage.success('设备已退役')
    fetchDevices()
  } catch (e) { if (e !== 'cancel') ElMessage.error(e.response?.data?.detail || '操作失败') }
}

const activateDevice = async (row) => {
  try {
    await ElMessageBox.confirm(`确认启用设备 ${row.device_code}？`)
    await request.put(`/devices/${encodeURIComponent(row.device_code)}/activate`)
    ElMessage.success('设备已启用')
    fetchDevices()
  } catch (e) { if (e !== 'cancel') ElMessage.error(e.response?.data?.detail || '操作失败') }
}

const onImportSuccess = (res) => {
  ElMessage.success(`导入成功：${res.success_rows}/${res.total_rows} 行，${res.failed_rows} 行失败`)
  fetchDevices()
}

const onImportError = () => { ElMessage.error('导入失败') }

onMounted(() => { fetchDevices(); fetchCodeRules() })
</script>

<style scoped>
.page { padding: 20px; }
.page-header { margin-bottom: 16px; }
</style>