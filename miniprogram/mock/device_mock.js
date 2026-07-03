/**
 * 设备档案 Mock 数据
 * 字段名、数据类型严格遵循 PRD 数据库设计
 * device_code 格式：CSGZ-{线别}-{站别}-{设备号}
 * result_status 仅使用 pass / fail
 */
const deviceMockData = [
    {
        device_code: 'CSGZ-A01-DBC-01',
        device_name: '数控车床 #1',
        location: 'A车间-加工区-01工位',
        template_id: 1,
        qr_url: 'https://example.com/qr/CSGZ-A01-DBC-01.png'
    },
    {
        device_code: 'CSGZ-A01-DBC-02',
        device_name: '数控车床 #2',
        location: 'A车间-加工区-02工位',
        template_id: 1,
        qr_url: 'https://example.com/qr/CSGZ-A01-DBC-02.png'
    },
    {
        device_code: 'CSGZ-A02-WT-01',
        device_name: '卧式加工中心 #1',
        location: 'A车间-精加工区-01工位',
        template_id: 2,
        qr_url: 'https://example.com/qr/CSGZ-A02-WT-01.png'
    },
    {
        device_code: 'CSGZ-A02-WT-02',
        device_name: '卧式加工中心 #2',
        location: 'A车间-精加工区-02工位',
        template_id: 2,
        qr_url: 'https://example.com/qr/CSGZ-A02-WT-02.png'
    },
    {
        device_code: 'CSGZ-A03-PT-01',
        device_name: '空压机 #1',
        location: 'B车间-动力站-01位',
        template_id: 3,
        qr_url: 'https://example.com/qr/CSGZ-A03-PT-01.png'
    },
    {
        device_code: 'CSGZ-A03-PT-02',
        device_name: '空压机 #2',
        location: 'B车间-动力站-02位',
        template_id: 3,
        qr_url: 'https://example.com/qr/CSGZ-A03-PT-02.png'
    },
    {
        device_code: 'CSGZ-A04-MMIT-01',
        device_name: '三坐标测量机',
        location: 'C车间-质检区-01位',
        template_id: 4,
        qr_url: 'https://example.com/qr/CSGZ-A04-MMIT-01.png'
    },
    {
        device_code: 'CSGZ-A05-CAT-01',
        device_name: '自动化装配线 #1',
        location: 'D车间-装配区-01线',
        template_id: 5,
        qr_url: 'https://example.com/qr/CSGZ-A05-CAT-01.png'
    },
    {
        device_code: 'CSGZ-P01-AT-01',
        device_name: '热处理炉 #1',
        location: 'E车间-热处理区-01位',
        template_id: 6,
        qr_url: 'https://example.com/qr/CSGZ-P01-AT-01.png'
    },
    {
        device_code: 'CSGZ-P05-MT-01',
        device_name: '铣床 #1',
        location: 'A车间-铣削区-01工位',
        template_id: 7,
        qr_url: 'https://example.com/qr/CSGZ-P05-MT-01.png'
    },
    {
        device_code: 'CSGZ-S01-RSE-01',
        device_name: '冷却水循环泵 #1',
        location: 'F车间-公用工程-01位',
        template_id: 8,
        qr_url: 'https://example.com/qr/CSGZ-S01-RSE-01.png'
    },
    {
        device_code: 'CSGZ-S02-UT-01',
        device_name: '环保废气处理系统',
        location: 'F车间-环保区-01位',
        template_id: 9,
        qr_url: 'https://example.com/qr/CSGZ-S02-UT-01.png'
    }
];

/**
 * 工程师在后台为各技术员分配设备（技术员只有执行权限）
 * 模拟工程师分配的映射关系
 */
const techDeviceAssignment = {
    1: ["CSGZ-A01-DBC-01", "CSGZ-A01-DBC-02", "CSGZ-A02-WT-01", "CSGZ-A02-WT-02"],
    2: ["CSGZ-A03-PT-01", "CSGZ-A03-PT-02", "CSGZ-A04-MMIT-01", "CSGZ-A05-CAT-01", "CSGZ-P01-AT-01"],
    3: ["CSGZ-P05-MT-01", "CSGZ-S01-RSE-01", "CSGZ-S02-UT-01"]
};

/**
 * 今日待点检任务列表（模拟技术员视角）
 * 技术员不感知分配逻辑，只接收工程师分配好的设备列表
 * 前2台已点检，后几台未点检（模拟今日任务状态）
 */
const getTodayTasks = (techId) => {
    const assignedCodes = techDeviceAssignment[techId] || [];
    const assignedDevices = deviceMockData.filter(d => assignedCodes.includes(d.device_code));
    // 模拟：前2台已点检，剩余的为今日待点检
    return assignedDevices.slice(2);
};

/**
 * 根据 device_code 查询设备信息
 */
const getDeviceByCode = (deviceCode) => {
    return deviceMockData.find(d => d.device_code === deviceCode) || null;
};

module.exports = {
    deviceMockData,
    getTodayTasks,
    getDeviceByCode
};