/**
 * 微信登录 Mock 数据
 * 模拟3个技术员账号（工程师在后台分配设备，技术员只有执行权限）
 */
const mockUsers = [
    {
        id: 1,
        username: "tech_001",
        real_name: "张师傅",
        role: "tech",
        device_codes: [
            "CSGZ-A01-DBC-01", "CSGZ-A01-DBC-02",
            "CSGZ-A02-WT-01", "CSGZ-A02-WT-02"
        ]
    },
    {
        id: 2,
        username: "tech_002",
        real_name: "李师傅",
        role: "tech",
        device_codes: [
            "CSGZ-A03-PT-01", "CSGZ-A03-PT-02",
            "CSGZ-A04-MMIT-01", "CSGZ-A05-CAT-01",
            "CSGZ-P01-AT-01"
        ]
    },
    {
        id: 3,
        username: "tech_003",
        real_name: "王师傅",
        role: "tech",
        device_codes: [
            "CSGZ-P05-MT-01",
            "CSGZ-S01-RSE-01",
            "CSGZ-S02-UT-01"
        ]
    }
];

/**
 * Mock 微信登录
 * 根据 code 后两位数字取模选择用户
 * 实际生产环境应调用微信接口获取 openid 后查库
 */
function mockWechatLogin(code) {
    // 根据 code 的 hash 选择用户（模拟不同技术员扫码登录不同账号）
    const hash = code.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0);
    const userIndex = hash % 3;
    const user = { ...mockUsers[userIndex] };

    // 生成模拟 Token
    const token = `mock_token_${user.id}_${Date.now()}`;

    return {
        access_token: token,
        token_type: "bearer",
        user_id: user.id,
        username: user.username,
        real_name: user.real_name,
        role: user.role,
        device_codes: user.device_codes
    };
}

/**
 * 获取用户负责的设备编码列表
 */
function getUserDeviceCodes(userId) {
    const user = mockUsers.find(u => u.id === userId);
    return user ? user.device_codes : [];
}

module.exports = {
    mockUsers,
    mockWechatLogin,
    getUserDeviceCodes
};