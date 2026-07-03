"""
点检执行相关 API 路由
POST /api/v1/inspection/submit       提交点检结果
GET  /api/v1/inspection/today_tasks  技术员查看今日未点检设备列表
PUT  /api/v1/inspection/remark/{id}  工程师对异常记录追加备注
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
import json
import os
import uuid

from app.database import get_db
from app.models.inspection_record import InspectionRecord, ResultStatus
from app.models.device import Device
from app.models.user import User, UserRole
from app.schemas.inspection import InspectionSubmitRequest, EngineerRemarkRequest
from app.api.v1.auth import get_current_user_id, get_current_user_role
from app.config import settings
from app.utils.watermark import add_watermark

router = APIRouter(prefix="/inspection", tags=["点检执行"])


@router.post("/submit", summary="提交点检结果")
async def submit_inspection(
    device_code: str = Form(...),
    gps_lat: float = Form(...),
    gps_lng: float = Form(...),
    items: str = Form(...),
    result_status: str = Form(...),
    remark: Optional[str] = Form(None),
    photos: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    提交点检结果
    - 含图片上传（自动叠加水印）
    - GPS 位置信息
    - result_status 仅允许 pass/fail
    """
    # 验证设备存在
    device = db.query(Device).filter(Device.device_code == device_code).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"设备 {device_code} 不存在")

    # 验证 result_status
    if result_status not in ("pass", "fail"):
        raise HTTPException(status_code=400, detail="result_status 必须为 pass 或 fail")

    # fail 时 remark 必填
    if result_status == "fail" and not remark:
        raise HTTPException(status_code=400, detail="异常记录必须填写异常原因 (remark)")

    # 处理图片上传与水印
    photo_urls = []
    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)

    for photo in photos:
        # 生成唯一文件名
        file_ext = photo.filename.split(".")[-1] if "." in photo.filename else "jpg"
        unique_name = f"{uuid.uuid4().hex}.{file_ext}"
        temp_path = os.path.join(upload_dir, unique_name)

        # 保存临时文件
        content = await photo.read()
        with open(temp_path, "wb") as f:
            f.write(content)

        # 叠加水印
        watermark_text = f"{device_code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        watermarked_path = os.path.join(upload_dir, f"wm_{unique_name}")
        add_watermark(temp_path, watermarked_path, watermark_text)

        # 删除临时文件
        os.remove(temp_path)

        # 保存水印后图片的相对路径
        photo_urls.append(f"/static/uploads/wm_{unique_name}")

    # 解析 items JSON
    try:
        items_data = json.loads(items)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="items 格式错误，需为有效 JSON")

    # 创建点检记录
    record = InspectionRecord(
        device_code=device_code,
        tech_id=user_id,
        check_time=datetime.now(),
        gps_lat=gps_lat,
        gps_lng=gps_lng,
        photo_urls=photo_urls,
        result_status=ResultStatus(result_status),
        remark=remark,
        is_deleted=0
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "message": "点检提交成功",
        "record_id": record.id,
        "result_status": result_status,
        "photo_count": len(photo_urls)
    }


@router.get("/today_tasks", summary="技术员查看今日未点检设备列表")
def get_today_tasks(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    获取技术员今日尚未点检的设备列表
    """
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # 查询今日已点检的设备编号
    checked_codes = db.query(InspectionRecord.device_code).filter(
        InspectionRecord.tech_id == user_id,
        InspectionRecord.check_time >= today_start,
        InspectionRecord.is_deleted == 0
    ).distinct().all()
    checked_set = {code[0] for code in checked_codes}

    # 获取所有未点检设备（过滤已退役设备）
    all_devices = db.query(Device).filter(Device.is_deleted == 0).all()
    unchecked_devices = [
        device.to_dict() for device in all_devices
        if device.device_code not in checked_set
    ]

    return {
        "total_today": len(all_devices),
        "checked_count": len(checked_set),
        "unchecked_count": len(unchecked_devices),
        "tasks": unchecked_devices
    }


@router.put("/remark/{record_id}", summary="工程师对异常记录追加备注")
def add_engineer_remark(
    record_id: int,
    request: EngineerRemarkRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_role)
):
    """
    工程师对异常记录追加备注（仅追加模式）
    仅 engineer 角色可操作
    """
    if current_user["role"] != "engineer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅工程师可追加备注"
        )

    record = db.query(InspectionRecord).filter(
        InspectionRecord.id == record_id,
        InspectionRecord.is_deleted == 0
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")

    # 仅追加模式：保留原有备注，追加新内容
    if record.engineer_remark:
        record.engineer_remark += f"\n--- 工程师 {current_user['real_name']} 追加 ---\n{request.engineer_remark}"
    else:
        record.engineer_remark = f"工程师 {current_user['real_name']}:\n{request.engineer_remark}"

    db.commit()
    db.refresh(record)

    return {
        "message": "备注已追加",
        "record_id": record.id,
        "engineer_remark": record.engineer_remark
    }


@router.get("/records", summary="技术员查看本人最近点检记录")
def get_my_records(
    limit: int = 20,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    技术员查看本人提交的最近点检记录
    """
    records = db.query(InspectionRecord).filter(
        InspectionRecord.tech_id == user_id,
        InspectionRecord.is_deleted == 0
    ).order_by(
        InspectionRecord.check_time.desc()
    ).limit(limit).all()

    return [record.to_dict() for record in records]