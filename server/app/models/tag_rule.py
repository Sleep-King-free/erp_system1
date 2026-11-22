"""标签规则表模型。"""
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class TagRule(Base):
    __tablename__ = "tag_rules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    keyword: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="命中关键字（如：扩产）"
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id"), nullable=False, index=True, comment="关联标签"
    )
