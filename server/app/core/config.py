"""应用配置。

通过 pydantic-settings 从环境变量与 .env 文件加载配置，
字段名与 .env 中的变量名一一对应（区分大小写）。
"""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# 项目根目录（server/）
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # 项目信息
    PROJECT_NAME: str = "ERP System"
    API_V1_PREFIX: str = "/api/v1"

    # 数据库连接（MySQL + PyMySQL 驱动）
    DATABASE_URL: str = "mysql+pymysql://root:password@127.0.0.1:3306/erp?charset=utf8mb4"

    # 安全相关
    SECRET_KEY: str = ""  # 生产环境务必通过 .env 配置为随机字符串
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # AI 大模型（OpenAI 兼容接口，如 OpenAI/DeepSeek/通义/智谱等）
    AI_API_KEY: str = ""
    AI_BASE_URL: str = "https://api.openai.com/v1/chat/completions"
    AI_MODEL: str = "gpt-4o-mini"


@lru_cache
def get_settings() -> Settings:
    """返回缓存的配置实例，避免重复读取 .env 文件。"""
    return Settings()


settings = get_settings()
