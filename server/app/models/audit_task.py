"""审核任务表模型。"""
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AuditTask(Base):
    __tablename__ = "audit_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_reports.id"), nullable=False, index=True, comment="关联分析报告"
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PENDING",
        comment="状态：PENDING/CONFIRMED/REJECTED",
    )
    reviewer_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True, comment="审核人（关联用户）"
    )
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="审核备注")
