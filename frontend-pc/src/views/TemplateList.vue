<template>
  <div class="page">
    <div class="page-header">
      <el-button type="primary" @click="openCreate">新建模板</el-button>
    </div>
    <el-table :data="templates" stripe style="width:100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="template_name" label="模板名称" width="200" />
      <el-table-column prop="device_type" label="适用设备类型" width="150" />
      <el-table-column prop="item_count" label="项目数量" width="80" />
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column label="操作" min-width="200">
        <template #default="{ row }">
          <el-button type="primary" link size="small" @click="openEdit(row)">编辑</el-button>
          <el-button type="warning" link size="small" @click="handleCopy(row)">复制</el-button>
          <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialog.visible" :title="dialog.isEdit ? '编辑模板' : '新建模板'" width="700px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="模板名称" required>
          <el-input v-model="form.template_name" placeholder="请输入模板名称" />
        </el-form-item>
        <el-form-item label="设备类型">
          <el-input v-model="form.device_type" placeholder="例如：车床类" />
        </el-form-item>
        <el-form-item label="点检项目">
          <div v-for="(item, idx) in form.items" :key="idx" class="item-row">
            <el-input v-model="item.item_name" placeholder="项目名称" style="width:150px;margin-right:8px" />
            <el-select v-model="item.data_type" style="width:120px;margin-right:8px">
              <el-option label="数值" value="number" />
              <el-option label="布尔" value="boolean" />
              <el-option label="文本" value="text" />
            </el-select>
            <el-input-number v-if="item.data_type==='number'" v-model="item.standard_min" :min="0" placeholder="下限" style="width:100px;margin-right:8px" controls-position="right" />
            <el-input-number v-if="item.data_type==='number'" v-model="item.standard_max" :min="0" placeholder="上限" style="width:100px;margin-right:8px" controls-position="right" />
            <el-input v-if="item.data_type==='number'" v-model="item.unit" placeholder="单位" style="width:70px;margin-right:8px" />
            <el-button type="danger" :icon="Delete" circle size="small" @click="removeItem(idx)" />
          </div>
          <el-button type="primary" link @click="addItem">+ 添加项目</el-button>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog.visible=false">取消</el-button>
        <el-button type="primary" @click="saveTemplate">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete } from '@element-plus/icons-vue'
import request from '@/api/request.js'

const templates = ref([])
const dialog = reactive({ visible: false, isEdit: false, editId: null })
const form = reactive({ template_name: '', device_type: '', items: [] })

const fetchTemplates = async () => {
  try { templates.value = await request.get('/templates/list') }
  catch (e) { ElMessage.error('加载模板失败') }
}

const openCreate = () => {
  dialog.isEdit = false; dialog.editId = null; dialog.visible = true
  form.template_name = ''; form.device_type = ''; form.items = []
}

const openEdit = async (row) => {
  dialog.isEdit = true; dialog.editId = row.id; dialog.visible = true
  try {
    const detail = await request.get(`/templates/${row.id}`)
    form.template_name = detail.template_name
    form.device_type = detail.device_type || ''
    form.items = (detail.items || []).map(i => ({
      item_name: i.item_name,
      data_type: i.data_type,
      standard_min: i.standard_min,
      standard_max: i.standard_max,
      unit: i.unit || ''
    }))
  } catch (e) { ElMessage.error('加载模板详情失败') }
}

const addItem = () => {
  form.items.push({ item_name: '', data_type: 'number', standard_min: null, standard_max: null, unit: '' })
}

const removeItem = (idx) => { form.items.splice(idx, 1) }

const saveTemplate = async () => {
  if (!form.template_name.trim()) { ElMessage.warning('请输入模板名称'); return }
  if (form.items.length === 0) { ElMessage.warning('请添加至少一个点检项目'); return }
  try {
    if (dialog.isEdit) {
      await request.put(`/templates/${dialog.editId}`, form)
    } else {
      await request.post('/templates', form)
    }
    ElMessage.success(dialog.isEdit ? '模板已更新' : '模板已创建')
    dialog.visible = false
    fetchTemplates()
  } catch (e) { ElMessage.error(e.response?.data?.detail || '保存失败') }
}

const handleCopy = async (row) => {
  try {
    const detail = await request.get(`/templates/${row.id}`)
    const copyData = {
      template_name: detail.template_name + '_副本',
      device_type: detail.device_type,
      items: (detail.items || []).map(i => ({
        item_name: i.item_name, data_type: i.data_type,
        standard_min: i.standard_min, standard_max: i.standard_max, unit: i.unit || ''
      }))
    }
    await request.post('/templates', copyData)
    ElMessage.success('模板已复制')
    fetchTemplates()
  } catch (e) { ElMessage.error('复制失败') }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确认删除模板"${row.template_name}"？`)
    await request.delete(`/templates/${row.id}`)
    ElMessage.success('模板已删除')
    fetchTemplates()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(e.response?.data?.detail || '删除失败')
  }
}

onMounted(fetchTemplates)
</script>

<style scoped>
.page { padding: 20px; }
.page-header { margin-bottom: 16px; }
.item-row { display: flex; align-items: center; margin-bottom: 8px; }
</style>