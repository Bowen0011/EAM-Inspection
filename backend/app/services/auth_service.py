"""
认证服务层
处理用户登录、微信登录、密码加密验证
"""
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.models.user import User, UserRole
from app.utils.jwt_handler import create_access_token
from app.config import settings
from typing import Optional


def hash_password(password: str) -> str:
    """使用 bcrypt 加密密码"""
    return bcrypt.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return bcrypt.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    账号密码认证
    返回用户对象或 None
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def create_user_token(user: User) -> dict:
    """
    为用户生成 JWT Token
    """
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "role": user.role.value if user.role else "",
            "real_name": user.real_name
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "real_name": user.real_name,
        "role": user.role.value if user.role else ""
    }


def init_admin_user(db: Session):
    """
    初始化管理员账号
    如果数据库中不存在管理员账号，则创建
    """
    admin = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
    if not admin:
        admin = User(
            username=settings.ADMIN_USERNAME,
            password_hash=hash_password(settings.ADMIN_PASSWORD),
            role=UserRole.ENGINEER,
            real_name="系统管理员"
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)


def handle_wechat_login(db: Session, code: str) -> Optional[dict]:
    """
    微信小程序登录（Mock 模式）
    实际生产中应调用微信接口获取 openid
    """
    # Mock 模式：根据 code 生成模拟 openid
    mock_openid = f"mock_openid_{code[:8]}" if code else "mock_openid_default"

    # 查找是否已有该 openid 的用户
    user = db.query(User).filter(User.wechat_openid == mock_openid).first()

    if not user:
        # 创建新用户（默认角色为技术员）
        user = User(
            username=f"tech_{mock_openid[-6:]}",
            password_hash=hash_password("123456"),
            role=UserRole.TECH,
            real_name=f"技术员_{mock_openid[-4:]}",
            wechat_openid=mock_openid
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return create_user_token(user)