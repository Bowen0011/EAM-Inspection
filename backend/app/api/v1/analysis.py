"""
数据分析相关 API 路由
GET /api/v1/analysis/dashboard      工程师首页看板
GET /api/v1/analysis/export_excel   导出周报/月报 Excel
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, date
from typing import Optional

from app.database import get_db
from app.models.inspection_record import InspectionRecord, ResultStatus
from app.models.device import Device
from app.models.user import User, UserRole
from app.api.v1.auth import get_current_user_role
from app.utils.excel_export import generate_report_excel

router = APIRouter(prefix="/analysis", tags=["数据分析"])


@router.get("/dashboard", summary="工程师首页看板")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_role)
):
    """
    工程师首页看板
    - 总设备数
    - 今日点检率
    - 待处理异常数（result_status=fail 且工程师尚未处理）
    - 最新异常列表
    """
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    # 总设备数
    total_devices = db.query(func.count(Device.device_code)).scalar()

    # 今日点检记录数
    today_records = db.query(func.count(InspectionRecord.id)).filter(
        InspectionRecord.check_time >= today_start,
        InspectionRecord.check_time < today_end,
        InspectionRecord.is_deleted == 0
    ).scalar()

    # 今日点检率（已点检设备数 / 总设备数）
    today_checked_devices = db.query(func.count(func.distinct(InspectionRecord.device_code))).filter(
        InspectionRecord.check_time >= today_start,
        InspectionRecord.check_time < today_end,
        InspectionRecord.is_deleted == 0
    ).scalar()

    inspection_rate = round((today_checked_devices / total_devices * 100), 1) if total_devices > 0 else 0

    # 待处理异常数（fail 且工程师尚未处理）
    pending_abnormal = db.query(func.count(InspectionRecord.id)).filter(
        InspectionRecord.result_status == ResultStatus.FAIL,
        InspectionRecord.is_deleted == 0,
        InspectionRecord.engineer_remark.is_(None)
    ).scalar()

    # 最新异常列表（取最近10条 fail 记录）
    latest_abnormal = db.query(InspectionRecord).filter(
        InspectionRecord.result_status == ResultStatus.FAIL,
        InspectionRecord.is_deleted == 0
    ).order_by(
        InspectionRecord.check_time.desc()
    ).limit(10).all()

    # 设备名称映射
    devices = {d.device_code: d.device_name for d in db.query(Device).all()}
    tech_users = {u.id: u.real_name for u in db.query(User).filter(User.role == UserRole.TECH).all()}

    abnormal_list = []
    for record in latest_abnormal:
        abnormal_list.append({
            "id": record.id,
            "device_code": record.device_code,
            "device_name": devices.get(record.device_code, "未知设备"),
            "tech_name": tech_users.get(record.tech_id, f"技术员#{record.tech_id}"),
            "check_time": record.check_time.isoformat() if record.check_time else None,
            "remark": record.remark,
            "engineer_remark": record.engineer_remark
        })

    return {
        "total_devices": total_devices,
        "today_records": today_records,
        "today_checked_devices": today_checked_devices,
        "inspection_rate": inspection_rate,
        "pending_abnormal": pending_abnormal,
        "latest_abnormal": abnormal_list
    }


@router.get("/trend", summary="获取点检趋势数据")
def get_trend(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_role)
):
    """
    获取指定天数内的点检完成率趋势
    """
    total_devices = db.query(func.count(Device.device_code)).scalar()
    if total_devices == 0:
        return {"dates": [], "completion_rates": []}

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    dates = []
    rates = []

    for i in range(days - 1, -1, -1):
        day_start = today - timedelta(days=i)
        day_end = day_start + timedelta(days=1)

        checked_count = db.query(func.count(func.distinct(InspectionRecord.device_code))).filter(
            InspectionRecord.check_time >= day_start,
            InspectionRecord.check_time < day_end,
            InspectionRecord.is_deleted == 0
        ).scalar()

        rate = round((checked_count / total_devices * 100), 1) if total_devices > 0 else 0
        dates.append(day_start.strftime("%Y-%m-%d"))
        rates.append(rate)

    return {"dates": dates, "completion_rates": rates}


@router.get("/export_excel", summary="导出周报/月报 Excel")
def export_excel(
    start_date: str,
    end_date: str,
    tech_name: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_role)
):
    """
    导出点检报告 Excel
    - start_date: 开始日期 (YYYY-MM-DD)
    - end_date: 结束日期 (YYYY-MM-DD)
    - tech_name: 可选，按技术员姓名筛选
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD")

    # 查询点检记录
    query = db.query(InspectionRecord).filter(
        InspectionRecord.check_time >= start,
        InspectionRecord.check_time <= end,
        InspectionRecord.is_deleted == 0
    )

    if tech_name:
        user = db.query(User).filter(User.real_name == tech_name).first()
        if user:
            query = query.filter(InspectionRecord.tech_id == user.id)

    records = query.order_by(InspectionRecord.check_time.desc()).all()

    # 生成 Excel 文件流
    excel_data = generate_report_excel(records, start_date, end_date, db)

    from fastapi.responses import Response
    return Response(
        content=excel_data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=点检报表_{start_date}_{end_date}.xlsx"
        }
    )