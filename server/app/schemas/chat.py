"""聊天记录相关 Pydantic 模型。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChatRecordCreate(BaseModel):
    """创建聊天记录的请求体。"""

    customer_id: int
    content: str


class ChatRecordOut(BaseModel):
    """聊天记录的响应模型。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    content: str
    channel: str | None = None
    occurred_at: datetime | None = None
