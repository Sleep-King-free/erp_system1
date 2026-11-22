"""分析报告相关 Pydantic 模型。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnalysisReportCreate(BaseModel):
    """触发 AI 分析的请求体。"""

    customer_id: int


class AnalysisFieldOut(BaseModel):
    """字段级可信度与原文依据。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    field_key: str
    value: str | None = None
    credibility: int | None = None
    source_text: str | None = None


class AnalysisReportResponse(BaseModel):
    """返回给前端的分析报告详情（含性格、建议、字段级可信度）。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    version: int
    summary: str | None = None
    personality_type: str | None = None
    personality_analysis: str | None = None
    companion_advice: str | None = None
    action_suggestions: str | None = None
    created_at: datetime
    fields: list[AnalysisFieldOut] = []
