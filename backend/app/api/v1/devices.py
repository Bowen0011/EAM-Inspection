"""
设备管理相关 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
import openpyxl
import io

from app.database import get_db
from app.models.device import Device
from app.models.inspection_item import InspectionItem
from app.api.v1.auth import get_current_user_id, get_current_user_role
from app.api.v1.deps import require_permission

router = APIRouter(prefix="/devices", tags=["设备管理"])

LINE_OPTIONS = [
    "A01","A02","A03","A04","A05","A06","A07",
    "P01","P02","P03","P04","P05","P06","P07",
    "S01","S02"
]
STATION_OPTIONS = [
    "DBC","WT","PT","MMIT","CAT","AT","MT",
    "RSE","UT","CW","MC","MMIS","MMI1"
]


@router.get("/info/{code}", summary="扫码获取设备信息+关联模板")
def get_device_info(code: str, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    device = db.query(Device).filter(Device.device_code == code).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"设备 {code} 不存在")

    template_items = db.query(InspectionItem).filter(
        InspectionItem.template_id == device.template_id
    ).all()

    return {
        "device": device.to_dict(),
        "template_items": [item.to_dict() for item in template_items]
    }


@router.get("/code-rules", summary="获取设备编码规则")
def get_device_code_rules():
    return {
        "department": "CSGZ",
        "line_options": LINE_OPTIONS,
        "station_options": STATION_OPTIONS,
        "device_number_pattern": "01-99"
    }


@router.get("/list", summary="获取设备列表（支持分页）")
def list_devices(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    include_deleted: bool = False,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user_role)
):
    query = db.query(Device)
    if not include_deleted:
        query = query.filter(Device.is_deleted == 0)

    total = query.count()
    devices = query.order_by(Device.device_code).offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "devices": [d.to_dict() for d in devices]
    }


@router.put("/{code}/retire", summary="退役设备")
def retire_device(
    code: str,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permission("devices:manage"))
):
    device = db.query(Device).filter(Device.device_code == code).first()
    if not device:
        raise HTTPException(status_code=404, detail="设备不存在")
    if device.is_deleted:
        raise HTTPException(status_code=400, detail="该设备已退役")
    device.is_deleted = 1
    db.commit()
    return {"message": "设备已退役", "device_code": code}


@router.put("/{code}/activate", summary="启用设备")
def activate_device(
    code: str,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permission("devices:manage"))
):
    device = db.query(Device).filter(Device.device_code == code).first()
    if not device:
        raise HTTPException(status_code=404, detail="设备不存在")
    if not device.is_deleted:
        raise HTTPException(status_code=400, detail="该设备已是启用状态")
    device.is_deleted = 0
    db.commit()
    return {"message": "设备已启用", "device_code": code}


@router.post("/import", summary="批量导入设备（Excel）")
def import_devices(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: dict = Depends(require_permission("devices:manage"))
):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="请上传 .xlsx 或 .xls 格式的Excel文件")

    content = file.file.read()
    wb = openpyxl.load_workbook(io.BytesIO(content))
    ws = wb.active

    total_rows = 0
    success_rows = 0
    errors = []

    for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        total_rows += 1
        line = str(row[0]).strip().upper() if row[0] else ""
        station = str(row[1]).strip().upper() if row[1] else ""
        device_no = str(row[2]).strip() if row[2] else ""
        device_name = str(row[3]).strip() if row[3] else ""

        # 校验线别
        if line not in LINE_OPTIONS:
            errors.append({"row": row_idx, "reason": f"线别 {line} 不在字典范围内"})
            continue
        # 校验站别
        if station not in STATION_OPTIONS:
            errors.append({"row": row_idx, "reason": f"站别 {station} 不在字典范围内"})
            continue
        # 校验设备号
        try:
            num = int(device_no)
            if num < 1 or num > 99:
                errors.append({"row": row_idx, "reason": f"设备号 {device_no} 超出 01~99 范围"})
                continue
            device_no = f"{num:02d}"
        except ValueError:
            errors.append({"row": row_idx, "reason": f"设备号 {device_no} 格式错误"})
            continue
        # 校验设备名称
        if not device_name:
            errors.append({"row": row_idx, "reason": "设备名称为空"})
            continue

        device_code = f"CSGZ-{line}-{station}-{device_no}"

        # 唯一性校验
        existing = db.query(Device).filter(Device.device_code == device_code).first()
        if existing:
            errors.append({"row": row_idx, "reason": f"设备编号 {device_code} 已存在"})
            continue

        # 导入
        device = Device(
            device_code=device_code,
            device_name=device_name,
            location=f"{line}线-{station}",
            template_id=1,
            is_deleted=0
        )
        db.add(device)
        success_rows += 1

    db.commit()
    return {
        "total_rows": total_rows,
        "success_rows": success_rows,
        "failed_rows": len(errors),
        "errors": errors
    }