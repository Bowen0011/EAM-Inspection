const api = require('../../utils/api.js');

Page({
    data: {
        tasks: [],
        taskCount: 0
    },

    onShow() {
        const app = getApp();
        if (!app.checkLogin()) return;
        this.loadTasks();
    },

    onPullDownRefresh() {
        this.loadTasks(() => {
            wx.stopPullDownRefresh();
        });
    },

    loadTasks(callback) {
        const app = getApp();
        const userId = app.globalData.userId;
        api.getTodayTasks(userId).then(res => {
            const tasks = res.tasks || [];
            this.setData({
                tasks: tasks,
                taskCount: tasks.length
            });
            if (callback) callback();
        }).catch(err => {
            console.error('加载任务失败:', err);
            wx.showToast({ title: '加载失败', icon: 'none' });
            if (callback) callback();
        });
    },

    onScanTap(e) {
        const deviceCode = e.currentTarget.dataset.deviceCode;
        const app = getApp();

        // Mock 模式：直接跳转，跳过真实扫码
        if (app.globalData.useMock !== false) {
            wx.navigateTo({
                url: `/pages/inspect/inspect?device_code=${deviceCode}`
            });
            return;
        }

        // 真实模式：调用微信扫码
        wx.scanCode({
            onlyFromCamera: true,
            success: (res) => {
                const scannedCode = res.result;
                wx.navigateTo({
                    url: `/pages/inspect/inspect?device_code=${scannedCode}`
                });
            },
            fail: () => {
                wx.showToast({ title: '扫码失败，请重试', icon: 'none' });
            }
        });
    }
});