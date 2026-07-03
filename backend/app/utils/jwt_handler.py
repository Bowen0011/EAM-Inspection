"""
JWT Token 生成与验证工具
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from app.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    生成 JWT Token
    :param data: 需要编码的数据（必须包含 sub 字段）
    :param expires_delta: 过期时间，默认使用配置中的时间
    :return: JWT Token 字符串
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    验证 JWT Token
    :param token: JWT Token 字符串
    :return: 如果验证成功返回 payload 字典，否则返回 None
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None