"""标签相关 Pydantic 模型（增删改查）。"""
from pydantic import BaseModel, ConfigDict


class TagCreate(BaseModel):
    """创建标签。"""

    name: str
    category: str | None = None


class TagUpdate(BaseModel):
    """更新标签。"""

    name: str | None = None
    category: str | None = None


class TagOut(BaseModel):
    """标签响应模型。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str | None = None


class TagRuleCreate(BaseModel):
    """创建标签规则。"""

    keyword: str
    tag_id: int


class TagRuleUpdate(BaseModel):
    """更新标签规则。"""

    keyword: str | None = None
    tag_id: int | None = None


class TagRuleOut(BaseModel):
    """标签规则响应模型。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    keyword: str
    tag_id: int
