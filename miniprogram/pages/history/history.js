const api = require('../../utils/api.js');
Page({
    data: { records: [] },
    onShow() {
        const app = getApp();
        if (!app.checkLogin()) return;
        const userId = app.globalData.userId;
        api.getHistory(userId).then(res => {
            this.setData({ records: res.records || [] });
        }).catch(err => {
            console.error('加载历史失败:', err);
        });
    },
    onCardTap(e) {
        const id = e.currentTarget.dataset.id;
        wx.navigateTo({ url: `/pages/detail/detail?id=${id}` });
    }
});