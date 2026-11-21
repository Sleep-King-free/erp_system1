"""聊天记录表模型。"""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class ChatRecord(Base):
    __tablename__ = "chat_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"), nullable=False, index=True, comment="所属客户"
    )
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="聊天内容")
    channel: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="来源渠道")
    occurred_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="发生时间"
    )
