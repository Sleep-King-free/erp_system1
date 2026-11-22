"""订单表模型。"""
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"), nullable=False, index=True, comment="所属客户"
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, comment="订单金额"
    )
    order_date: Mapped[date] = mapped_column(Date, nullable=False, comment="订单日期")
    sales_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, comment="跟进业务员（关联用户）"
    )
