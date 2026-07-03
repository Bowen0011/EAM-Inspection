/**
 * 统一 API 请求层
 * 支持 Mock/Real 模式切换
 * USE_MOCK = true 时拦截请求返回 Mock 数据
 * USE_MOCK = false 时通过 wx.request 调用真实后端
 */
const USE_MOCK = true; // 开发阶段 true，联调时改为 false

// Mock 数据模块
const authMock = require('../mock/auth_mock.js');
const deviceMock = require('../mock/device_mock.js');
const templateMock = require('../mock/template_mock.js');
const historyMock = require('../mock/history_mock.js');

/**
 * Mock 模式：微信登录
 */
function mockWechatLogin(code) {
    return new Promise((resolve) => {
        const result = authMock.mockWechatLogin(code);
        resolve(result);
    });
}

/**
 * Mock 模式：获取今日待点检任务
 */
function mockGetTodayTasks(userId) {
    return new Promise((resolve) => {
        const tasks = deviceMock.getTodayTasks(userId);
        resolve({ tasks });
    });
}

/**
 * Mock 模式：扫码获取设备信息（含模板）
 */
function mockGetDeviceInfo(deviceCode) {
    return new Promise((resolve) => {
        const device = deviceMock.getDeviceByCode(deviceCode);
        if (!device) {
            resolve({ error: '设备不存在' });
            return;
        }
        const template = templateMock.getTemplateById(device.template_id);
        resolve({
            device: device,
            template_items: template ? template.items : []
        });
    });
}

/**
 * Mock 模式：提交点检结果
 */
function mockSubmitInspection(payload) {
    return new Promise((resolve) => {
        console.log('[Mock] 点检提交 payload:', JSON.stringify(payload, null, 2));
        resolve({
            message: '点检提交成功（Mock）',
            record_id: Date.now(),
            result_status: payload.result_status,
            photo_count: (payload.photos || []).length
        });
    });
}

/**
 * Mock 模式：获取历史记录
 */
function mockGetHistory(userId) {
    return new Promise((resolve) => {
        const records = historyMock.getHistoryByTechId(userId);
        resolve({ records });
    });
}

/**
 * Mock 模式：获取记录详情
 */
function mockGetDetail(recordId) {
    return new Promise((resolve) => {
        const detail = historyMock.getDetailById(recordId);
        resolve(detail || { error: '记录不存在' });
    });
}

// ========== 真实 API 请求（后续联调时启用） ==========
const BASE_URL = 'http://localhost:8000/api/v1';

function realRequest(method, path, data = null, token = '') {
    return new Promise((resolve, reject) => {
        const header = { 'Content-Type': 'application/json' };
        if (token) {
            header['Authorization'] = `Bearer ${token}`;
        }
        wx.request({
            url: `${BASE_URL}${path}`,
            method: method,
            header: header,
            data: data,
            success: (res) => resolve(res.data),
            fail: (err) => reject(err)
        });
    });
}

// ========== 统一导出接口 ==========

/**
 * 微信登录
 */
function wechatLogin(code) {
    if (USE_MOCK) return mockWechatLogin(code);
    return realRequest('POST', '/auth/wechat_login', { code });
}

/**
 * 获取今日待点检任务
 */
function getTodayTasks(userId) {
    if (USE_MOCK) return mockGetTodayTasks(userId);
    return realRequest('GET', `/inspection/today_tasks?user_id=${userId}`);
}

/**
 * 扫码获取设备信息+关联模板
 */
function getDeviceInfo(deviceCode) {
    if (USE_MOCK) return mockGetDeviceInfo(deviceCode);
    const app = getApp();
    return realRequest('GET', `/devices/info/${deviceCode}`, null, app.globalData.token);
}

/**
 * 提交点检结果
 */
function submitInspection(payload) {
    if (USE_MOCK) return mockSubmitInspection(payload);
    const app = getApp();
    return realRequest('POST', '/inspection/submit', payload, app.globalData.token);
}

/**
 * 获取历史记录
 */
function getHistory(userId) {
    if (USE_MOCK) return mockGetHistory(userId);
    const app = getApp();
    return realRequest('GET', `/inspection/records?limit=20`, null, app.globalData.token);
}

/**
 * 获取记录详情
 */
function getDetail(recordId) {
    if (USE_MOCK) return mockGetDetail(recordId);
    // 真实 API 尚无详情接口，可复用 records 后前端过滤
    return Promise.reject('真实API详情接口待实现');
}

module.exports = {
    wechatLogin,
    getTodayTasks,
    getDeviceInfo,
    submitInspection,
    getHistory,
    getDetail
};