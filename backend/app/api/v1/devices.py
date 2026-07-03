"""
设备管理相关 API 路由
GET  /api/v1/devices/info/{code}   扫码获取设备信息+关联模板
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.device import Device
from app.models.inspection_item import InspectionItem
from app.api.v1.auth import get_current_user_id

router = APIRouter(prefix="/devices", tags=["设备管理"])


@router.get("/info/{code}", summary="扫码获取设备信息+关联模板")
def get_device_info(code: str, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """
    根据设备编号查询设备信息和关联的点检模板明细
    """
    device = db.query(Device).filter(Device.device_code == code).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"设备 {code} 不存在"
        )

    # 查询关联的点检模板项目
    template_items = db.query(InspectionItem).filter(
        InspectionItem.template_id == device.template_id
    ).all()

    return {
        "device": device.to_dict(),
        "template_items": [item.to_dict() for item in template_items]
    }


@router.get("/code-rules", summary="获取设备编码规则")
def get_device_code_rules():
    """
    返回设备编码规则（线别、站别的可选列表）
    用于前端渲染下拉选择框
    """
    return {
        "department": "CSGZ",
        "line_options": [
            "A01", "A02", "A03", "A04", "A05", "A06", "A07",
            "P01", "P02", "P03", "P04", "P05", "P06", "P07",
            "S01", "S02"
        ],
        "station_options": [
            "DBC", "WT", "PT", "MMIT", "CAT", "AT", "MT",
            "RSE", "UT", "CW", "MC", "MMIS", "MMI1"
        ],
        "device_number_pattern": "01-99"
    }