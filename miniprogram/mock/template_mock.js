/**
 * 点检模板明细 Mock 数据
 * 字段名、数据类型严格遵循 PRD 数据库设计
 * data_type 仅使用 number / boolean / text
 * result_status 仅使用 pass / fail
 */

// 模板 1：数控车床点检项目
const template1 = {
    template_id: 1,
    template_name: '数控车床日常点检',
    items: [
        {
            id: 101,
            template_id: 1,
            item_name: '主轴温度',
            data_type: 'number',
            standard_min: 20.0,
            standard_max: 65.0,
            unit: '℃'
        },
        {
            id: 102,
            template_id: 1,
            item_name: '润滑油位',
            data_type: 'boolean',
            standard_min: null,
            standard_max: null,
            unit: ''
        },
        {
            id: 103,
            template_id: 1,
            item_name: '冷却液压力',
            data_type: 'number',
            standard_min: 0.3,
            standard_max: 0.6,
            unit: 'MPa'
        },
        {
            id: 104,
            template_id: 1,
            item_name: '异响检查',
            data_type: 'boolean',
            standard_min: null,
            standard_max: null,
            unit: ''
        },
        {
            id: 105,
            template_id: 1,
            item_name: '刀具磨损情况',
            data_type: 'text',
            standard_min: null,
            standard_max: null,
            unit: ''
        }
    ]
};

// 模板 2：卧式加工中心点检项目
const template2 = {
    template_id: 2,
    template_name: '卧式加工中心日常点检',
    items: [
        {
            id: 201,
            template_id: 2,
            item_name: '主轴转速',
            data_type: 'number',
            standard_min: 0,
            standard_max: 8000,
            unit: 'rpm'
        },
        {
            id: 202,
            template_id: 2,
            item_name: '导轨润滑油位',
            data_type: 'boolean',
            standard_min: null,
            standard_max: null,
            unit: ''
        },
        {
            id: 203,
            template_id: 2,
            item_name: '液压系统压力',
            data_type: 'number',
            standard_min: 4.0,
            standard_max: 7.0,
            unit: 'MPa'
        },
        {
            id: 204,
            template_id: 2,
            item_name: '冷却液温度',
            data_type: 'number',
            standard_min: 10.0,
            standard_max: 40.0,
            unit: '℃'
        }
    ]
};

// 模板 3：空压机点检项目
const template3 = {
    template_id: 3,
    template_name: '空压机日常点检',
    items: [
        {
            id: 301,
            template_id: 3,
            item_name: '排气温度',
            data_type: 'number',
            standard_min: 60.0,
            standard_max: 100.0,
            unit: '℃'
        },
        {
            id: 302,
            template_id: 3,
            item_name: '油位正常',
            data_type: 'boolean',
            standard_min: null,
            standard_max: null,
            unit: ''
        },
        {
            id: 303,
            template_id: 3,
            item_name: '排水阀状态',
            data_type: 'boolean',
            standard_min: null,
            standard_max: null,
            unit: ''
        },
        {
            id: 304,
            template_id: 3,
            item_name: '运行电流',
            data_type: 'number',
            standard_min: 10.0,
            standard_max: 50.0,
            unit: 'A'
        }
    ]
};

// 模板 4：三坐标测量机
const template4 = {
    template_id: 4,
    template_name: '三坐标测量机日常点检',
    items: [
        {
            id: 401,
            template_id: 4,
            item_name: '气浮压力',
            data_type: 'number',
            standard_min: 0.4,
            standard_max: 0.6,
            unit: 'MPa'
        },
        {
            id: 402,
            template_id: 4,
            item_name: '环境温度',
            data_type: 'number',
            standard_min: 18.0,
            standard_max: 22.0,
            unit: '℃'
        },
        {
            id: 403,
            template_id: 4,
            item_name: '测头校准状态',
            data_type: 'boolean',
            standard_min: null,
            standard_max: null,
            unit: ''
        }
    ]
};

// 模板 5：自动化装配线
const template5 = {
    template_id: 5,
    template_name: '自动化装配线日常点检',
    items: [
        {
            id: 501,
            template_id: 5,
            item_name: '输送带速度',
            data_type: 'number',
            standard_min: 1.0,
            standard_max: 5.0,
            unit: 'm/min'
        },
        {
            id: 502,
            template_id: 5,
            item_name: '气压值',
            data_type: 'number',
            standard_min: 0.5,
            standard_max: 0.8,
            unit: 'MPa'
        },
        {
            id: 503,
            template_id: 5,
            item_name: '传感器状态',
            data_type: 'boolean',
            standard_min: null,
            standard_max: null,
            unit: ''
        },
        {
            id: 504,
            template_id: 5,
            item_name: '急停按钮状态',
            data_type: 'boolean',
            standard_min: null,
            standard_max: null,
            unit: ''
        }
    ]
};

// 模板 6：热处理炉
const template6 = {
    template_id: 6,
    template_name: '热处理炉日常点检',
    items: [
        {
            id: 601,
            template_id: 6,
            item_name: '炉内温度',
            data_type: 'number',
            standard_min: 200.0,
            standard_max: 1200.0,
            unit: '℃'
        },
        {
            id: 602,
            template_id: 6,
            item_name: '保温时间',
            data_type: 'number',
            standard_min: 0.5,
            standard_max: 8.0,
            unit: 'h'
        },
        {
            id: 603,
            template_id: 6,
            item_name: '炉门密封状态',
            data_type: 'boolean',
            standard_min: null,
            standard_max: null,
            unit: ''
        }
    ]
};

// 模板 7：铣床
const template7 = {
    template_id: 7,
    template_name: '铣床日常点检',
    items: [
        {
            id: 701,
            template_id: 7,
            item_name: '主轴振动值',
            data_type: 'number',
            standard_min: 0,
            standard_max: 5.0,
            unit: 'mm/s'
        },
        {
            id: 702,
            template_id: 7,
            item_name: '工作台润滑',
            data_type: 'boolean',
            standard_min: null,
            standard_max: null,
            unit: ''
        },
        {
            id: 703,
            template_id: 7,
            item_name: '冷却液状态',
            data_type: 'boolean',
            standard_min: null,
            standard_max: null,
            unit: ''
        }
    ]
};

// 模板 8：冷却水循环泵
const template8 = {
    template_id: 8,
    template_name: '冷却水循环泵日常点检',
    items: [
        {
            id: 801,
            template_id: 8,
            item_name: '出口压力',
            data_type: 'number',
            standard_min: 0.2,
            standard_max: 0.5,
            unit: 'MPa'
        },
        {
            id: 802,
            template_id: 8,
            item_name: '电机温度',
            data_type: 'number',
            standard_min: 20.0,
            standard_max: 75.0,
            unit: '℃'
        },
        {
            id: 803,
            template_id: 8,
            item_name: '密封泄漏',
            data_type: 'boolean',
            standard_min: null,
            standard_max: null,
            unit: ''
        }
    ]
};

// 模板 9：环保废气处理系统
const template9 = {
    template_id: 9,
    template_name: '环保废气处理系统日常点检',
    items: [
        {
            id: 901,
            template_id: 9,
            item_name: '风机电流',
            data_type: 'number',
            standard_min: 5.0,
            standard_max: 30.0,
            unit: 'A'
        },
        {
            id: 902,
            template_id: 9,
            item_name: '活性炭压差',
            data_type: 'number',
            standard_min: 0,
            standard_max: 2.0,
            unit: 'kPa'
        },
        {
            id: 903,
            template_id: 9,
            item_name: '排放风机运行',
            data_type: 'boolean',
            standard_min: null,
            standard_max: null,
            unit: ''
        }
    ]
};

// 所有模板映射
const templateMap = {
    1: template1,
    2: template2,
    3: template3,
    4: template4,
    5: template5,
    6: template6,
    7: template7,
    8: template8,
    9: template9
};

/**
 * 根据 template_id 获取模板明细
 */
const getTemplateById = (templateId) => {
    return templateMap[templateId] || null;
};

/**
 * 获取所有模板列表
 */
const getAllTemplates = () => {
    return Object.values(templateMap);
};

module.exports = {
    templateMap,
    getTemplateById,
    getAllTemplates
};