"""标签字典表模型。"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, comment="标签名称"
    )
    category: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="标签分类")
