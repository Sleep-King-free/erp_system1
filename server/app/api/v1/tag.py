"""标签与规则接口。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Tag, TagRule
from app.schemas.tag import (
    TagCreate,
    TagOut,
    TagRuleCreate,
    TagRuleOut,
    TagRuleUpdate,
    TagUpdate,
)

router = APIRouter(prefix="/api/v1", tags=["tag"])


# ---- 标签 CRUD ----


@router.post("/tags", response_model=TagOut, status_code=201)
def create_tag(payload: TagCreate, db: Session = Depends(get_db)):
    """新增标签。"""
    tag = Tag(**payload.model_dump())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.get("/tags", response_model=list[TagOut])
def list_tags(db: Session = Depends(get_db)):
    """标签列表。"""
    return db.scalars(select(Tag).order_by(Tag.id)).all()


@router.get("/tags/{tag_id}", response_model=TagOut)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    """标签详情。"""
    tag = db.get(Tag, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="标签不存在")
    return tag


@router.put("/tags/{tag_id}", response_model=TagOut)
def update_tag(tag_id: int, payload: TagUpdate, db: Session = Depends(get_db)):
    """更新标签。"""
    tag = db.get(Tag, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="标签不存在")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(tag, field, value)
    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/tags/{tag_id}", status_code=204)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """删除标签。"""
    tag = db.get(Tag, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="标签不存在")
    db.delete(tag)
    db.commit()


# ---- 规则 CRUD ----


@router.post("/tag-rules", response_model=TagRuleOut, status_code=201)
def create_tag_rule(payload: TagRuleCreate, db: Session = Depends(get_db)):
    """新增关键字打标规则。"""
    if db.get(Tag, payload.tag_id) is None:
        raise HTTPException(status_code=404, detail="关联标签不存在")
    rule = TagRule(**payload.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


@router.get("/tag-rules", response_model=list[TagRuleOut])
def list_tag_rules(db: Session = Depends(get_db)):
    """规则列表。"""
    return db.scalars(select(TagRule).order_by(TagRule.id)).all()


@router.put("/tag-rules/{rule_id}", response_model=TagRuleOut)
def update_tag_rule(rule_id: int, payload: TagRuleUpdate, db: Session = Depends(get_db)):
    """更新规则。"""
    rule = db.get(TagRule, rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="规则不存在")
    if payload.tag_id is not None and db.get(Tag, payload.tag_id) is None:
        raise HTTPException(status_code=404, detail="关联标签不存在")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(rule, field, value)
    db.commit()
    db.refresh(rule)
    return rule


@router.delete("/tag-rules/{rule_id}", status_code=204)
def delete_tag_rule(rule_id: int, db: Session = Depends(get_db)):
    """删除规则。"""
    rule = db.get(TagRule, rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="规则不存在")
    db.delete(rule)
    db.commit()
