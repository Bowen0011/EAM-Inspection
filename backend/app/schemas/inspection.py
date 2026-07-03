"""
点检相关的 Pydantic 请求/响应模型
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class InspectionItemValue(BaseModel):
    """点检项目值"""
    item_id: int = Field(..., description="项目ID")
    item_name: str = Field(..., description="项目名")
    value: str = Field(..., description="填入的值（数字转字符串/布尔转字符串/文本）")
    is_abnormal: bool = Field(default=False, description="是否异常")


class InspectionSubmitRequest(BaseModel):
    """提交点检结果请求"""
    device_code: str = Field(..., description="设备编号")
    gps_lat: Decimal = Field(..., ge=-90, le=90, description="纬度")
    gps_lng: Decimal = Field(..., ge=-180, le=180, description="经度")
    items: List[InspectionItemValue] = Field(..., min_length=1, description="点检项目值列表")
    result_status: str = Field(..., pattern=r"^(pass|fail)$", description="pass(合格)/fail(异常)")
    remark: Optional[str] = Field(None, description="异常原因（fail时必填）")


class InspectionRecordResponse(BaseModel):
    """点检记录响应"""
    id: int
    device_code: str
    tech_id: int
    check_time: datetime
    gps_lat: Optional[float] = None
    gps_lng: Optional[float] = None
    photo_urls: Optional[List[str]] = None
    result_status: str
    remark: Optional[str] = None
    engineer_remark: Optional[str] = None
    is_deleted: int = 0


class EngineerRemarkRequest(BaseModel):
    """工程师追加备注请求（仅追加模式）"""
    engineer_remark: str = Field(..., min_length=1, max_length=1000, description="工程师意见")