"""
用户表 (users)
"""
from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, Enum as SAEnum
from app.database import Base
from datetime import datetime
import enum


class UserRole(str, enum.Enum):
    TECH = "tech"        # 技术员
    ENGINEER = "engineer"  # 工程师
    STORE = "store"       # 库管


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True, comment="登录名")
    password_hash = Column(String(255), nullable=False, comment="加密存储")
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.TECH, comment="角色")
    real_name = Column(String(20), nullable=False, comment="真实姓名")
    wechat_openid = Column(String(100), nullable=True, unique=True, comment="小程序登录唯一标识")
    is_active = Column(SmallInteger, nullable=False, default=1, comment="启用/禁用 1启用 0禁用")
    last_login_at = Column(DateTime, nullable=True, comment="最近登录时间")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role.value if self.role else None,
            "real_name": self.real_name,
            "wechat_openid": self.wechat_openid,
            "is_active": self.is_active,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None
        }
