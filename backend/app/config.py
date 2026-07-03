"""
应用配置管理
从 .env 文件和环境变量读取配置
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # MySQL 配置
    MYSQL_HOST: str = "mysql"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "eam_user"
    MYSQL_PASSWORD: str = "eam_pass_2024"
    MYSQL_DATABASE: str = "eam_inspection"

    # SQLite 模式（本地开发/演示用）
    USE_SQLITE: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 处理 .env 文件中字符串转 bool
        if isinstance(self.USE_SQLITE, str):
            self.USE_SQLITE = self.USE_SQLITE.lower() in ("true", "1", "yes")

    @property
    def DATABASE_URL(self) -> str:
        if self.USE_SQLITE:
            return "sqlite:///./eam_demo.db"
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"

    # Redis 配置
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # JWT 配置
    JWT_SECRET_KEY: str = "your-jwt-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24小时

    # 微信小程序
    WECHAT_APPID: Optional[str] = "mock_appid"
    WECHAT_SECRET: Optional[str] = "mock_secret"

    # 文件上传
    UPLOAD_DIR: str = "/app/uploads"
    MAX_UPLOAD_SIZE_MB: int = 10

    # 管理员初始账号
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123456"

    # .env 中存在的其他配置项
    MYSQL_ROOT_PASSWORD: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()