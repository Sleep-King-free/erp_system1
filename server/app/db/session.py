"""数据库连接与会话管理（SQLAlchemy 2.0 风格）。"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # 每次取连接前先检测连接是否有效，避免 MySQL 断连报错
    pool_recycle=3600,    # 连接空闲超过 1 小时后自动回收
    echo=False,           # 生产环境建议关闭 SQL 日志，调试时可临时改为 True
)

# 会话工厂：后续用 SessionLocal() 创建 session
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# 全局 Base 类，供 models 中的 ORM 模型继承
Base = declarative_base()


def get_db():
    """FastAPI 依赖注入：获取数据库 session，请求结束后自动关闭。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
