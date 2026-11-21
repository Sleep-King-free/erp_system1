"""审核任务表模型。"""
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AuditTask(Base):
    __tablename__ = "audit_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    snapshot_id: Mapped[int] = mapped_column(
        ForeignKey("profile_snapshots.id"), nullable=False, index=True, comment="关联画像快照"
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
