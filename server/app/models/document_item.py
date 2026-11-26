"""单据明细表模型（一张单据下面的多行货物）。"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class DocumentItem(Base):
    __tablename__ = "document_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"), nullable=False, index=True, comment="所属单据"
    )
    line_no: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, comment="原单据上的行号，从 1 开始"
    )
    product_name: Mapped[str | None] = mapped_column(
        String(200), nullable=True, comment="品名"
    )
    spec: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="规格"
    )
    unit: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="单位"
    )
    quantity: Mapped[float | None] = mapped_column(
        Numeric(12, 3), nullable=True, comment="数量"
    )
    unit_price: Mapped[float | None] = mapped_column(
        Numeric(14, 2), nullable=True, comment="单价"
    )
    amount: Mapped[float | None] = mapped_column(
        Numeric(14, 2), nullable=True, comment="金额（数量×单价）"
    )
    remark: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="备注"
    )
    is_valid: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="是否有效行（数量为空判为无效）"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), comment="创建时间"
    )
