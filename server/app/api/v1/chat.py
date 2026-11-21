"""聊天记录接口。"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import ChatRecord, Customer
from app.schemas.chat import ChatRecordCreate, ChatRecordOut

router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.post("/chat-records", response_model=ChatRecordOut, status_code=201)
def create_chat_record(payload: ChatRecordCreate, db: Session = Depends(get_db)):
    """新增聊天记录。"""
    if db.get(Customer, payload.customer_id) is None:
        raise HTTPException(status_code=404, detail="客户不存在")

    record = ChatRecord(
        customer_id=payload.customer_id,
        content=payload.content,
        occurred_at=datetime.now(),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/chat-records", response_model=list[ChatRecordOut])
def list_chat_records(customer_id: int, db: Session = Depends(get_db)):
    """根据客户 id 获取历史聊天记录。"""
    records = db.scalars(
        select(ChatRecord)
        .where(ChatRecord.customer_id == customer_id)
        .order_by(ChatRecord.id)
    ).all()
    return records
