<template>
  <div class="dashboard">
    <el-row :gutter="20" class="stat-row">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-label">总设备数</div>
            <div class="stat-value">{{ stats.total_devices }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-label">今日点检率</div>
            <div class="stat-value" :style="{color: stats.inspection_rate >= 80 ? '#67c23a' : '#e6a23c'}">
              {{ stats.inspection_rate }}%
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-label">待处理异常</div>
            <div class="stat-value" style="color:#f56c6c;animation:blink 1s infinite">
              {{ stats.pending_abnormal }}
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-label">今日点检数</div>
            <div class="stat-value">{{ stats.today_records }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card shadow="hover" class="chart-card">
      <template #header>
        <span>近7日点检趋势</span>
      </template>
      <div ref="chartRef" style="height: 300px"></div>
    </el-card>

    <el-card shadow="hover" class="table-card">
      <template #header>
        <span>最新异常记录</span>
      </template>
      <el-table :data="stats.latest_abnormal || []" stripe style="width:100%">
        <el-table-column prop="device_code" label="设备编号" width="200" />
        <el-table-column prop="device_name" label="设备名称" width="150" />
        <el-table-column prop="tech_name" label="技术员" width="100" />
        <el-table-column prop="check_time" label="时间" width="180" />
        <el-table-column prop="remark" label="异常原因" min-width="200" show-overflow-tooltip />
        <el-table-column label="处理" width="150">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="openRemarkDialog(row)">
              处理
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="remarkDialog.visible" title="处理异常" width="500px">
      <el-form>
        <el-form-item label="设备编号">{{ remarkDialog.record?.device_code }}</el-form-item>
        <el-form-item label="异常原因">{{ remarkDialog.record?.remark }}</el-form-item>
        <el-form-item label="工程师意见">
          <el-input v-model="remarkDialog.remark" type="textarea" :rows="4"
            placeholder="请输入处理意见" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="remarkDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitRemark">确认处理</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/api/request.js'
import * as echarts from 'echarts'

const chartRef = ref(null)
const stats = reactive({
  total_devices: 0, inspection_rate: 0,
  pending_abnormal: 0, today_records: 0, latest_abnormal: []
})
const remarkDialog = reactive({
  visible: false, record: null, remark: ''
})

const fetchDashboard = async () => {
  try {
    const res = await request.get('/analysis/dashboard')
    Object.assign(stats, res)
  } catch (e) { ElMessage.error('加载仪表盘失败') }
}

const fetchTrend = async () => {
  try {
    const res = await request.get('/analysis/trend', { params: { days: 7 } })
    nextTick(() => {
      if (!chartRef.value) return
      const chart = echarts.init(chartRef.value)
      chart.setOption({
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: res.dates },
        yAxis: { type: 'value', max: 100, axisLabel: { formatter: '{value}%' } },
        series: [{
          data: res.completion_rates,
          type: 'line',
          smooth: true,
          areaStyle: { color: 'rgba(26,115,232,0.1)' },
          lineStyle: { color: '#1a73e8', width: 3 },
          itemStyle: { color: '#1a73e8' }
        }]
      })
    })
  } catch (e) { console.error('趋势加载失败', e) }
}

const openRemarkDialog = (record) => {
  remarkDialog.record = record
  remarkDialog.remark = ''
  remarkDialog.visible = true
}

const submitRemark = async () => {
  if (!remarkDialog.remark.trim()) {
    ElMessage.warning('请输入处理意见')
    return
  }
  try {
    await request.put(`/inspection/remark/${remarkDialog.record.id}`, {
      engineer_remark: remarkDialog.remark
    })
    ElMessage.success('处理成功')
    remarkDialog.visible = false
    fetchDashboard()
  } catch (e) { ElMessage.error('处理失败') }
}

onMounted(() => { fetchDashboard(); fetchTrend() })
</script>

<style scoped>
.dashboard { padding: 20px; }
.stat-row { margin-bottom: 20px; }
.stat-card { text-align: center; padding: 10px 0; }
.stat-label { font-size: 14px; color: #909399; margin-bottom: 8px; }
.stat-value { font-size: 32px; font-weight: bold; color: #303133; }
.chart-card, .table-card { margin-bottom: 20px; }
@keyframes blink { 50% { opacity: 0.5; } }
</style>