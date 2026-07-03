const api = require('../../utils/api.js')

Page({
    data: {
        tasks: [],
        taskCount: 0
    },

    onShow() {
        const app = getApp()
        if (!app.checkLogin()) return
        this.loadTasks()
    },

    onPullDownRefresh() {
        this.loadTasks(() => { wx.stopPullDownRefresh() })
    },

    loadTasks(callback) {
        const app = getApp()
        api.getTodayTasks(app.globalData.userId).then(res => {
            const tasks = res.tasks || []
            this.setData({ tasks, taskCount: tasks.length })
            if (callback) callback()
        }).catch(() => {
            wx.showToast({ title: '加载失败', icon: 'none' })
            if (callback) callback()
        })
    },

    onDeviceTap(e) {
        const device = e.currentTarget.dataset.device
        const app = getApp()

        if (app.globalData.useMock !== false) {
            wx.navigateTo({
                url: `/pages/inspect/inspect?device_code=${device.device_code}`
            })
            return
        }

        this.startScan()
    },

    startScan() {
        wx.scanCode({
            onlyFromCamera: true,
            scanType: ['qrCode'],
            success: (res) => {
                const code = (res.result || '').trim().toUpperCase()
                if (!this.validateDeviceCode(code)) {
                    wx.showToast({ title: '无效的设备二维码', icon: 'none' })
                    return
                }
                this.checkDeviceAndNavigate(code)
            },
            fail: (err) => {
                if (err && err.errMsg && err.errMsg.includes('cancel')) return
                wx.showModal({
                    title: '扫码失败',
                    content: '无法识别二维码，是否手动输入设备编号？',
                    confirmText: '手动输入',
                    success: (r) => { if (r.confirm) this.showManualInput() }
                })
            }
        })
    },

    showManualInput() {
        wx.showModal({
            title: '手动输入设备编号',
            editable: true,
            placeholderText: '例如：CSGZ-A01-DBC-01',
            success: (res) => {
                if (res.confirm && res.content) {
                    const code = res.content.trim().toUpperCase()
                    if (!this.validateDeviceCode(code)) {
                        wx.showToast({ title: '格式错误，应为 CSGZ-XXX-XXXX-XX', icon: 'none', duration: 3000 })
                        this.showManualInput()
                        return
                    }
                    this.checkDeviceAndNavigate(code)
                }
            }
        })
    },

    validateDeviceCode(code) {
        return /^CSGZ-[A-Z]\d{2}-[A-Z0-9]{4}-\d{2}$/.test(code)
    },

    checkDeviceAndNavigate(code) {
        wx.showLoading({ title: '验证设备...' })
        api.getDeviceInfo(code).then(res => {
            wx.hideLoading()
            if (!res || res.error) {
                wx.showToast({ title: '设备不存在', icon: 'none' })
                return
            }
            const device = res.device || {}
            if (device.is_deleted) {
                wx.showModal({
                    title: '设备已退役', showCancel: false,
                    content: `设备 ${code} 已退役，请联系管理员。`,
                    success: () => { this.loadTasks() }
                })
                return
            }
            wx.navigateTo({ url: `/pages/inspect/inspect?device_code=${code}` })
        }).catch(() => {
            wx.hideLoading()
            wx.showToast({ title: '网络异常', icon: 'none' })
        })
    }
})