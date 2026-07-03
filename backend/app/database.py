"""
数据库连接与会话管理
"""
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

_connect_args = {}
if settings.USE_SQLITE:
    _connect_args = {"check_same_thread": False}
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=NullPool,
        connect_args=_connect_args,
        echo=False
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 基类
Base = declarative_base()


def get_db():
    """
    获取数据库会话的依赖注入
    用于 FastAPI 的 Depends()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    初始化数据库表结构
    """
    Base.metadata.create_all(bind=engine)