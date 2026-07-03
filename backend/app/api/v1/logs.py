"""
操作日志查询 API 路由
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.models.operation_log import OperationLog
from app.api.v1.auth import get_current_user_role

router = APIRouter(prefix="/logs", tags=["操作日志"])


@router.get("/list", summary="获取操作日志列表")
def list_logs(
    operator_id: Optional[int] = None,
    module: Optional[str] = None,
    action_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_role)
):
    query = db.query(OperationLog)

    if operator_id:
        query = query.filter(OperationLog.operator_id == operator_id)
    if module:
        query = query.filter(OperationLog.module == module)
    if action_type:
        query = query.filter(OperationLog.action_type == action_type)
    if start_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(OperationLog.created_at >= start)
        except ValueError:
            pass
    if end_date:
        try:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(OperationLog.created_at <= end.replace(hour=23, minute=59, second=59))
        except ValueError:
            pass

    logs = query.order_by(OperationLog.created_at.desc()).limit(limit).all()
    return [log.to_dict() for log in logs]