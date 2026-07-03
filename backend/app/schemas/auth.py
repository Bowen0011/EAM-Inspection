"""
认证相关的 Pydantic 请求/响应模型
"""
from pydantic import BaseModel, Field
from typing import Optional


class LoginRequest(BaseModel):
    """账号密码登录请求"""
    username: str = Field(..., min_length=2, max_length=50, description="登录名")
    password: str = Field(..., min_length=6, max_length=100, description="密码")


class WechatLoginRequest(BaseModel):
    """微信小程序登录请求"""
    code: str = Field(..., description="微信登录临时code")


class TokenResponse(BaseModel):
    """登录成功响应"""
    access_token: str = Field(..., description="JWT Token")
    token_type: str = Field(default="bearer", description="Token类型")
    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., description="登录名")
    real_name: str = Field(..., description="真实姓名")
    role: str = Field(..., description="角色")


class UserInfoResponse(BaseModel):
    """用户信息响应"""
    id: int
    username: str
    role: str
    real_name: str
    wechat_openid: Optional[str] = None