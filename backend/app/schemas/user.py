"""
用户管理相关的 Pydantic 请求/响应模型
"""
from pydantic import BaseModel, Field
from typing import Optional


class UserListResponse(BaseModel):
    id: int
    username: str = Field(..., min_length=2, max_length=50)
    real_name: str
    role: str
    is_active: int
    last_login_at: Optional[str] = None
    must_change_password: int = 0


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6, max_length=100)


class UserStatusToggleRequest(BaseModel):
    is_active: bool


class PasswordResetResponse(BaseModel):
    message: str