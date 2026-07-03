const api = require('../../utils/api.js');
Page({
    data: { detail: {} },
    onLoad(options) {
        const id = parseInt(options.id);
        if (!id) { wx.showToast({ title: '参数错误', icon: 'none' }); return; }
        api.getDetail(id).then(res => {
            if (res) this.setData({ detail: res });
        }).catch(err => {
            console.error('加载详情失败:', err);
        });
    }
});