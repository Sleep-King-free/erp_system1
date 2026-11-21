"""模型包：统一导出所有 ORM 模型，供 Base.metadata.create_all 注册建表。"""
from app.models.audit_task import AuditTask
from app.models.chat_record import ChatRecord
from app.models.customer import Customer
from app.models.profile_snapshot import ProfileSnapshot
from app.models.user import User

__all__ = [
    "User",
    "Customer",
    "ChatRecord",
    "ProfileSnapshot",
    "AuditTask",
]
