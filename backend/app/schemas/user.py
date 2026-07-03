"""
用户管理相关的 Pydantic 请求/响应模型
"""
from pydantic import BaseModel
from typing import Optional


class UserListResponse(BaseModel):
    id: int
    username: str
    real_name: str
    role: str
    is_active: int
    last_login_at: Optional[str] = None


class UserStatusToggleRequest(BaseModel):
    is_active: bool


class PasswordResetResponse(BaseModel):
    message: str
    new_password: str = "123456"