"""
设备相关的 Pydantic 请求/响应模型
"""
from pydantic import BaseModel, Field
from typing import Optional


class DeviceInfoResponse(BaseModel):
    """设备信息响应（包含关联模板）"""
    device_code: str
    device_name: str
    location: str
    template_id: int
    qr_url: Optional[str] = None


class DeviceCreateRequest(BaseModel):
    """创建设备请求"""
    device_code: str = Field(..., pattern=r"^CSGZ-[A-Z0-9]{3}-[A-Z0-9]{4}-\d{2}$", description="设备编号")
    device_name: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=200)
    template_id: int = Field(..., ge=1)


class DeviceCodeRule(BaseModel):
    """设备编码规则说明"""
    department: str = "CSGZ"
    line_options: list = [
        "A01","A02","A03","A04","A05","A06","A07",
        "P01","P02","P03","P04","P05","P06","P07",
        "S01","S02"
    ]
    station_options: list = [
        "DBC","WT","PT","MMIT","CAT","AT","MT",
        "RSE","UT","CW","MC","MMIS","MMI1"
    ]
    device_number_range: str = "01-99"