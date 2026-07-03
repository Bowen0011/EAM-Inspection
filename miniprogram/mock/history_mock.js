/**
 * 历史点检记录 Mock 数据
 * 字段名、数据类型严格遵循 PRD 数据库设计
 * result_status 仅使用 pass / fail
 * 预置 8 条记录供前端展示
 */
const historyMockData = [
    {
        id: 1,
        device_code: "CSGZ-A01-DBC-01",
        device_name: "数控车床 #1",
        tech_id: 1,
        check_time: "2026-07-03 08:30:00",
        gps_lat: 23.1290745,
        gps_lng: 113.2643748,
        photo_urls: ["/static/uploads/wm_demo_01.jpg"],
        result_status: "pass",
        remark: "",
        engineer_remark: null,
        items: [
            { item_name: "主轴温度", value: "45.2", is_abnormal: false },
            { item_name: "润滑油位", value: "true", is_abnormal: false },
            { item_name: "冷却液压力", value: "0.45", is_abnormal: false },
            { item_name: "异响检查", value: "true", is_abnormal: false },
            { item_name: "刀具磨损情况", value: "正常", is_abnormal: false }
        ]
    },
    {
        id: 2,
        device_code: "CSGZ-A01-DBC-02",
        device_name: "数控车床 #2",
        tech_id: 1,
        check_time: "2026-07-03 08:45:00",
        gps_lat: 23.1290845,
        gps_lng: 113.2643848,
        photo_urls: ["/static/uploads/wm_demo_02.jpg"],
        result_status: "fail",
        remark: "主轴温度偏高，已超65℃，需要停机检查",
        engineer_remark: "已安排维修组检查冷却系统",
        items: [
            { item_name: "主轴温度", value: "78.5", is_abnormal: true },
            { item_name: "润滑油位", value: "true", is_abnormal: false },
            { item_name: "冷却液压力", value: "0.28", is_abnormal: true },
            { item_name: "异响检查", value: "true", is_abnormal: false },
            { item_name: "刀具磨损情况", value: "轻微磨损", is_abnormal: false }
        ]
    },
    {
        id: 3,
        device_code: "CSGZ-A02-WT-01",
        device_name: "卧式加工中心 #1",
        tech_id: 1,
        check_time: "2026-07-03 09:00:00",
        gps_lat: 23.1290945,
        gps_lng: 113.2643948,
        photo_urls: ["/static/uploads/wm_demo_03.jpg"],
        result_status: "pass",
        remark: "",
        engineer_remark: null,
        items: [
            { item_name: "主轴转速", value: "3500", is_abnormal: false },
            { item_name: "导轨润滑油位", value: "true", is_abnormal: false },
            { item_name: "液压系统压力", value: "5.2", is_abnormal: false },
            { item_name: "冷却液温度", value: "32.0", is_abnormal: false }
        ]
    },
    {
        id: 4,
        device_code: "CSGZ-A02-WT-02",
        device_name: "卧式加工中心 #2",
        tech_id: 1,
        check_time: "2026-07-02 16:30:00",
        gps_lat: 23.1291045,
        gps_lng: 113.2644048,
        photo_urls: ["/static/uploads/wm_demo_04.jpg"],
        result_status: "pass",
        remark: "",
        engineer_remark: null,
        items: [
            { item_name: "主轴转速", value: "4200", is_abnormal: false },
            { item_name: "导轨润滑油位", value: "true", is_abnormal: false },
            { item_name: "液压系统压力", value: "5.8", is_abnormal: false },
            { item_name: "冷却液温度", value: "35.0", is_abnormal: false }
        ]
    },
    {
        id: 5,
        device_code: "CSGZ-A03-PT-01",
        device_name: "空压机 #1",
        tech_id: 2,
        check_time: "2026-07-02 10:00:00",
        gps_lat: 23.1291145,
        gps_lng: 113.2644148,
        photo_urls: ["/static/uploads/wm_demo_05.jpg"],
        result_status: "fail",
        remark: "排气温度达102℃，超出标准上限100℃",
        engineer_remark: null,
        items: [
            { item_name: "排气温度", value: "102.3", is_abnormal: true },
            { item_name: "油位正常", value: "true", is_abnormal: false },
            { item_name: "排水阀状态", value: "true", is_abnormal: false },
            { item_name: "运行电流", value: "35.0", is_abnormal: false }
        ]
    },
    {
        id: 6,
        device_code: "CSGZ-A03-PT-02",
        device_name: "空压机 #2",
        tech_id: 2,
        check_time: "2026-07-02 10:15:00",
        gps_lat: 23.1291245,
        gps_lng: 113.2644248,
        photo_urls: ["/static/uploads/wm_demo_06.jpg"],
        result_status: "pass",
        remark: "",
        engineer_remark: null,
        items: [
            { item_name: "排气温度", value: "85.6", is_abnormal: false },
            { item_name: "油位正常", value: "true", is_abnormal: false },
            { item_name: "排水阀状态", value: "true", is_abnormal: false },
            { item_name: "运行电流", value: "28.0", is_abnormal: false }
        ]
    },
    {
        id: 7,
        device_code: "CSGZ-P05-MT-01",
        device_name: "铣床 #1",
        tech_id: 3,
        check_time: "2026-07-01 14:00:00",
        gps_lat: 23.1291345,
        gps_lng: 113.2644348,
        photo_urls: ["/static/uploads/wm_demo_07.jpg"],
        result_status: "pass",
        remark: "",
        engineer_remark: null,
        items: [
            { item_name: "主轴振动值", value: "2.3", is_abnormal: false },
            { item_name: "工作台润滑", value: "true", is_abnormal: false },
            { item_name: "冷却液状态", value: "true", is_abnormal: false }
        ]
    },
    {
        id: 8,
        device_code: "CSGZ-S02-UT-01",
        device_name: "环保废气处理系统",
        tech_id: 3,
        check_time: "2026-07-01 14:30:00",
        gps_lat: 23.1291445,
        gps_lng: 113.2644448,
        photo_urls: ["/static/uploads/wm_demo_08.jpg"],
        result_status: "fail",
        remark: "风机电流异常升高至32A，超出标准上限30A",
        engineer_remark: "已通知环保工程师现场处理",
        items: [
            { item_name: "风机电流", value: "32.5", is_abnormal: true },
            { item_name: "活性炭压差", value: "1.5", is_abnormal: false },
            { item_name: "排放风机运行", value: "true", is_abnormal: false }
        ]
    }
];

/**
 * 获取指定技术员的历史记录
 */
function getHistoryByTechId(techId) {
    return historyMockData.filter(r => r.tech_id === techId);
}

/**
 * 根据记录 ID 获取详情
 */
function getDetailById(recordId) {
    return historyMockData.find(r => r.id === recordId) || null;
}

module.exports = {
    historyMockData,
    getHistoryByTechId,
    getDetailById
};