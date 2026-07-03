/**
 * EAM-Inspection 企业点检管理系统
 * 微信小程序全局入口
 */
App({
    globalData: {
        userInfo: null,
        token: '',
        userId: 0,
        isLoggedIn: false
    },

    onLaunch() {
        // 尝试从缓存恢复登录状态
        const token = wx.getStorageSync('token');
        const userInfo = wx.getStorageSync('userInfo');
        if (token && userInfo) {
            this.globalData.token = token;
            this.globalData.userInfo = userInfo;
            this.globalData.userId = userInfo.id;
            this.globalData.isLoggedIn = true;
        }
    },

    /**
     * 检查登录态，未登录跳转登录页
     */
    checkLogin() {
        if (!this.globalData.isLoggedIn) {
            wx.redirectTo({ url: '/pages/login/login' });
            return false;
        }
        return true;
    },

    /**
     * 登录成功后设置全局状态
     */
    setLogin(token, userInfo) {
        this.globalData.token = token;
        this.globalData.userInfo = userInfo;
        this.globalData.userId = userInfo.id;
        this.globalData.isLoggedIn = true;
        wx.setStorageSync('token', token);
        wx.setStorageSync('userInfo', userInfo);
    },

    /**
     * 退出登录
     */
    logout() {
        this.globalData.token = '';
        this.globalData.userInfo = null;
        this.globalData.userId = 0;
        this.globalData.isLoggedIn = false;
        wx.removeStorageSync('token');
        wx.removeStorageSync('userInfo');
        wx.redirectTo({ url: '/pages/login/login' });
    }
});