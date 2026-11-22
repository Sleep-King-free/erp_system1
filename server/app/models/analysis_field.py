"""字段级可信度表模型。"""
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AnalysisField(Base):
    __tablename__ = "analysis_fields"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_reports.id"), nullable=False, index=True, comment="所属分析报告"
    )
    field_key: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="字段键（如 personality_type）"
    )
    value: Mapped[str | None] = mapped_column(Text, nullable=True, comment="字段值")
    credibility: Mapped[int | None] = mapped_column(nullable=True, comment="可信度（0-100）")
    source_text: Mapped[str | None] = mapped_column(Text, nullable=True, comment="原文依据")
