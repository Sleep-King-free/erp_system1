"""单据接口（第一版：先跑通，不落库）。"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["document"])


class DocumentDemoOut(BaseModel):
    """返回给前端的单据结构（暂时用假的）。"""

    document_type: str
    date: str
    partner: str
    total_amount: str
    items: list[dict]


@router.get("/documents/ping", response_model=DocumentDemoOut)
def ping_document():
    """连通性测试：确认单据接口已经挂上。"""
    return DocumentDemoOut(
        document_type="采购单",
        date="2026-11-22",
        partner="测试供应商",
        total_amount="82125",
        items=[
            {"品名": "货品A", "数量": "165", "单价": "105", "金额": "17325"},
        ],
    )


@router.get("/documents/ping/count")
def ping_count():
    """返回一个数字，最容易看出接口通没通。"""
    return {"count": 1, "message": "单据接口已挂载"}