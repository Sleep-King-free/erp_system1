"""模型包：统一导出所有 ORM 模型，供 Base.metadata.create_all 注册建表。"""
from app.models.analysis_field import AnalysisField
from app.models.analysis_report import AnalysisReport
from app.models.audit_task import AuditTask
from app.models.chat_record import ChatRecord
from app.models.customer import Customer
from app.models.document import Document
from app.models.document_item import DocumentItem
from app.models.order import Order
from app.models.tag import Tag
from app.models.tag_rule import TagRule
from app.models.user import User

__all__ = [
    "User",
    "Customer",
    "ChatRecord",
    "AnalysisReport",
    "AnalysisField",
    "AuditTask",
    "Document",
    "DocumentItem",
    "Order",
    "Tag",
    "TagRule",
]
