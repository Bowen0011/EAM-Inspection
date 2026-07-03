"""
报表导出 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from app.database import get_db
from app.models.inspection_record import InspectionRecord, ResultStatus
from app.models.device import Device
from app.models.user import User, UserRole
from app.api.v1.deps import require_permission
from app.utils.excel_export import generate_report_excel

router = APIRouter(prefix="/reports", tags=["报表导出"])


@router.get("/export", summary="导出点检报表 Excel")
def export_report(
    start_date: str,
    end_date: str,
    device_code: Optional[str] = None,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permission("reports:export"))
):
    """
    导出点检报表 Excel 文件
    - start_date: 开始日期 (YYYY-MM-DD)
    - end_date: 结束日期 (YYYY-MM-DD)
    - device_code: 可选，按设备编号筛选
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD")

    query = db.query(InspectionRecord).filter(
        InspectionRecord.check_time >= start,
        InspectionRecord.check_time <= end,
        InspectionRecord.is_deleted == 0
    )

    if device_code:
        query = query.filter(InspectionRecord.device_code == device_code)

    records = query.order_by(InspectionRecord.check_time.desc()).all()
    excel_data = generate_report_excel(records, start_date, end_date, db)

    return Response(
        content=excel_data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=点检报表_{start_date}_{end_date}.xlsx"
        }
    )