"""配置管理

基于 Pydantic Settings 的配置管理
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""

    # 应用信息
    APP_NAME: str = "User Management Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # 数据库配置
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/userdb"

    # 安全配置
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS 配置
    CORS_ORIGINS: list = ["*"]

    # 日志配置
    LOG_LEVEL: str = "INFO"

    class Config:
        """配置加载"""
        env_file = ".env"
        case_sensitive = True


# 全局配置实例
settings = Settings()
