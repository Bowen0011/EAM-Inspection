const api = require('../../utils/api.js');

Page({
    data: {
        deviceInfo: {},
        items: [],
        photos: [],
        photoTempFiles: [],
        isAbnormal: false,
        remark: '',
        gpsLat: null,
        gpsLng: null,
        submitDisabled: true,
        gpsLoaded: false
    },

    onLoad(options) {
        const deviceCode = options.device_code;
        if (!deviceCode) {
            wx.showToast({ title: '缺少设备编号', icon: 'none' });
            wx.navigateBack();
            return;
        }
        this.loadDeviceInfo(deviceCode);
        this.getGPS();
    },

    loadDeviceInfo(deviceCode) {
        api.getDeviceInfo(deviceCode).then(res => {
            if (!res || res.error) {
                wx.showToast({ title: '设备信息加载失败', icon: 'none' });
                return;
            }
            const items = (res.template_items || []).map(item => ({
                ...item,
                value: '',
                isError: false
            }));
            this.setData({
                deviceInfo: res.device,
                items: items
            });
            this.checkSubmitEnabled();
        });
    },

    getGPS() {
        wx.getLocation({
            type: 'wgs84',
            success: (res) => {
                this.setData({
                    gpsLat: res.latitude,
                    gpsLng: res.longitude,
                    gpsLoaded: true
                });
                this.checkSubmitEnabled();
            },
            fail: () => {
                wx.showToast({ title: '请打开定位权限', icon: 'none' });
                this.setData({ gpsLoaded: false });
                this.checkSubmitEnabled();
            }
        });
    },

    onNumberInput(e) {
        const idx = e.currentTarget.dataset.index;
        const value = e.detail.value;
        const numValue = parseFloat(value);
        const item = this.data.items[idx];
        let isError = false;
        if (!isNaN(numValue)) {
            if ((item.standard_min !== null && numValue < item.standard_min) ||
                (item.standard_max !== null && numValue > item.standard_max)) {
                isError = true;
            }
        }
        this.setData({
            [`items[${idx}].value`]: value,
            [`items[${idx}].isError`]: isError
        });
        this.checkSubmitEnabled();
    },

    onBooleanChange(e) {
        const idx = e.currentTarget.dataset.index;
        const checked = e.detail.value;
        this.setData({
            [`items[${idx}].value`]: checked ? 'true' : 'false'
        });
    },

    onTextInput(e) {
        const idx = e.currentTarget.dataset.index;
        this.setData({
            [`items[${idx}].value`]: e.detail.value
        });
    },

    onRemarkInput(e) {
        this.setData({ remark: e.detail.value });
        this.checkSubmitEnabled();
    },

    checkSubmitEnabled() {
        const { items, remark } = this.data;
        const hasError = items.some(item => item.isError === true);
        if (hasError) {
            this.setData({ isAbnormal: true, submitDisabled: !remark.trim() });
            return;
        }
        this.setData({ isAbnormal: false, submitDisabled: false });
    },

    onTakePhoto() {
        wx.chooseImage({
            count: 3,
            sourceType: ['camera'],
            success: (res) => {
                const tempFiles = res.tempFilePaths || [];
                this.setData({
                    photos: tempFiles,
                    photoTempFiles: tempFiles
                });
            },
            fail: () => {
                wx.showToast({ title: '拍摄失败', icon: 'none' });
            }
        });
    },

    onSubmit() {
        const { deviceInfo, items, gpsLat, gpsLng, remark, photos, gpsLoaded } = this.data;
        if (!gpsLoaded || !gpsLat) {
            wx.showToast({ title: '请开启定位权限', icon: 'none' });
            return;
        }
        const hasAnyAbnormal = items.some(item => item.isError);
        const resultStatus = hasAnyAbnormal ? 'fail' : 'pass';
        const payload = {
            device_code: deviceInfo.device_code,
            gps_lat: gpsLat,
            gps_lng: gpsLng,
            items: items.map(item => ({
                item_id: item.id,
                item_name: item.item_name,
                value: item.value,
                is_abnormal: item.isError || false
            })),
            result_status: resultStatus,
            remark: hasAnyAbnormal ? remark : '',
            photos: photos
        };
        console.log('[Mock] Submit payload:', JSON.stringify(payload, null, 2));
        api.submitInspection(payload).then(res => {
            wx.showToast({ title: '点检提交成功（Mock）', icon: 'success' });
            setTimeout(() => {
                wx.switchTab({ url: '/pages/home/home' });
            }, 1500);
        }).catch(err => {
            wx.showToast({ title: '提交失败', icon: 'none' });
        });
    }
});