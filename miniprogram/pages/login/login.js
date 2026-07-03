const api = require("../../utils/api.js");

Page({
  onWechatLogin() {
    wx.login({
      success: (res) => {
        if (res.code) {
          api.wechatLogin(res.code).then((result) => {
            const { token, userInfo, device_codes } = result;
            getApp().setLogin(token, userInfo);
            if (device_codes && device_codes.length) {
              wx.setStorageSync("device_codes", device_codes);
            }
            wx.switchTab({ url: "/pages/home/home" });
          }).catch((err) => {
            console.error("微信登录失败", err);
            wx.showToast({ title: "登录失败，请重试", icon: "none" });
          });
        } else {
          console.error("wx.login 获取 code 失败", res.errMsg);
          wx.showToast({ title: "登录失败，请重试", icon: "none" });
        }
      },
      fail: (err) => {
        console.error("wx.login 调用失败", err);
        wx.showToast({ title: "登录失败，请重试", icon: "none" });
      }
    });
  }
});
