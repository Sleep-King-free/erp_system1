"""FastAPI 主入口。"""
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import models  # noqa: F401  导入模型以注册到 Base.metadata，供 create_all 建表
from app.api.v1 import chat, document
from app.db.session import Base, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时自动创建所有数据表（演示阶段使用，后续替换为 Alembic 迁移）
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="智企盈辉 API", lifespan=lifespan)

# CORS 跨域中间件：允许所有来源，方便前端联调
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # 与 allow_origins=["*"] 搭配时不能设为 True
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat.router)
app.include_router(document.router)

@app.get("/")
def root():
    return {"message": "ERP系统后端服务启动成功"}


@app.get("/api/v1/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        version = db.execute(text("SELECT VERSION()")).scalar()
    except Exception as exc:  # noqa: BLE001 - 返回可读错误信息
        raise HTTPException(status_code=500, detail=f"数据库连接失败：{exc}")
    return {"message": "数据库连接成功", "mysql_version": version}

