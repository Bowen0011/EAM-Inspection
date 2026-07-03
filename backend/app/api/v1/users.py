"""
用户管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import random

from app.database import get_db
from app.models.user import User
from app.services.auth_service import hash_password
from app.api.v1.auth import get_current_user_role
from app.api.v1.deps import require_permission
from app.schemas.user import UserStatusToggleRequest

router = APIRouter(prefix="/users", tags=["账号管理"])


@router.get("/list", summary="获取用户列表")
def list_users(
    role: Optional[str] = None,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permission("users:manage"))
):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    users = query.order_by(User.id).all()
    return [u.to_dict() for u in users]


@router.post("/{user_id}/reset-password", summary="重置密码")
def reset_password(
    user_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permission("users:manage"))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 生成 6 位随机数字临时密码
    temp_password = str(random.randint(100000, 999999))
    user.password_hash = hash_password(temp_password)
    user.must_change_password = 1
    db.commit()

    return {"message": "密码已重置"}


@router.put("/{user_id}/toggle-status", summary="启用/禁用账号")
def toggle_user_status(
    user_id: int,
    request: UserStatusToggleRequest,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permission("users:manage"))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    user.is_active = 1 if request.is_active else 0
    db.commit()

    return {"message": "状态已更新", "is_active": bool(user.is_active)}