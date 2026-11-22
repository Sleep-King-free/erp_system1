"""客户分析报告表模型。"""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AnalysisReport(Base):
    __tablename__ = "analysis_reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"), nullable=False, index=True, comment="所属客户"
    )
    version: Mapped[int] = mapped_column(nullable=False, default=1, comment="报告版本号")
    summary: Mapped[str | None] = mapped_column(Text, nullable=True, comment="摘要")
    personality_type: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="DISC 性格类型：老虎型/孔雀型/考拉型/猫头鹰型"
    )
    personality_analysis: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="性格分析（基于 DISC）"
    )
    companion_advice: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="陪伴建议（不同性格的沟通策略）"
    )
    action_suggestions: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="行动建议（基于 BANT 和 DISC）"
    )
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True, comment="创建人（关联用户）"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), comment="创建时间"
    )
