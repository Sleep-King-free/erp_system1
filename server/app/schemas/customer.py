"""客户相关 Pydantic 模型。"""
from pydantic import BaseModel, ConfigDict


class CustomerCreate(BaseModel):
    """创建客户。"""

    name: str
    contact: str | None = None
    phone: str | None = None
    industry: str | None = None
    source: str | None = None
    owner_id: int
    importance_level: str = "普通"


class CustomerUpdate(BaseModel):
    """更新客户（部分字段，含重要性分级修改）。"""

    name: str | None = None
    contact: str | None = None
    phone: str | None = None
    industry: str | None = None
    source: str | None = None
    owner_id: int | None = None
    importance_level: str | None = None


class CustomerOut(BaseModel):
    """客户响应模型。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    contact: str | None = None
    phone: str | None = None
    industry: str | None = None
    source: str | None = None
    owner_id: int
    importance_level: str
