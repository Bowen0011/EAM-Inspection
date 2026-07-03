"""
点检模板相关的 Pydantic 请求/响应模型
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TemplateItemCreate(BaseModel):
    item_name: str = Field(..., min_length=1, max_length=50)
    data_type: str = Field(..., pattern=r"^(number|boolean|text)$")
    standard_min: Optional[float] = None
    standard_max: Optional[float] = None
    unit: Optional[str] = Field(None, max_length=10)


class TemplateCreateRequest(BaseModel):
    template_name: str = Field(..., min_length=1, max_length=50)
    device_type: Optional[str] = Field(None, max_length=50)
    items: List[TemplateItemCreate] = Field(..., min_length=1)


class TemplateListItemResponse(BaseModel):
    id: int
    template_name: str
    device_type: Optional[str] = None
    item_count: int = 0
    created_at: datetime


class TemplateDetailResponse(BaseModel):
    id: int
    template_name: str
    device_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: list = []