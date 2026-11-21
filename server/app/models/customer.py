"""客户表模型。"""
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True, comment="客户名称")
    contact: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="联系人")
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="联系电话")
    industry: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="所属行业")
    source: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="客户来源")
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True, comment="归属销售（关联用户）"
    )
