"""
认证相关 API 路由
POST /api/v1/auth/login         账号密码登录
POST /api/v1/auth/wechat_login  微信登录
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import LoginRequest, WechatLoginRequest, TokenResponse
from app.services.auth_service import authenticate_user, create_user_token, handle_wechat_login
from app.utils.jwt_handler import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

router = APIRouter(prefix="/auth", tags=["认证管理"])
security = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """
    从 JWT Token 中提取当前用户 ID
    用于需要登录的接口
    """
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的 Token 或 Token 已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = int(payload.get("sub"))
    return user_id


def get_current_user_role(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    从 JWT Token 中提取当前用户角色信息
    """
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的 Token 或 Token 已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "user_id": int(payload.get("sub")),
        "username": payload.get("username"),
        "role": payload.get("role"),
        "real_name": payload.get("real_name")
    }


@router.post("/login", response_model=TokenResponse, summary="账号密码登录")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    用户使用账号密码登录
    返回 JWT Token
    """
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_user_token(user)


@router.post("/wechat_login", response_model=TokenResponse, summary="微信小程序登录")
def wechat_login(request: WechatLoginRequest, db: Session = Depends(get_db)):
    """
    微信小程序端使用微信 code 登录
    返回 JWT Token（当前为 Mock 模式）
    """
    result = handle_wechat_login(db, request.code)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="微信登录失败",
        )
    return result