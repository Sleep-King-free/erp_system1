"""单据表模型（采购单/销售单）。"""
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    document_no: Mapped[str | None] = mapped_column(
        String(50), unique=True, nullable=True, index=True, comment="单据编号"
    )
    document_type: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="单据类型：采购单/销售单"
    )
    document_date: Mapped[date | None] = mapped_column(
        Date, nullable=True, comment="单据日期"
    )
    partner_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="往来单位名称"
    )
    total_amount: Mapped[float | None] = mapped_column(
        Numeric(14, 2), nullable=True, comment="合计金额"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="PENDING", comment="状态：PENDING/CONFIRMED"
    )
    source_image: Mapped[str | None] = mapped_column(
        String(255), nullable=True, comment="原始图片路径（OCR 识别用）"
    )
    remark: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="备注"
    )
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True, comment="创建人（关联用户）"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), comment="创建时间"
    )
