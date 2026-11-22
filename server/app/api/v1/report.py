"""分析报告接口。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import AnalysisReport, ChatRecord, Customer
from app.schemas.report import AnalysisReportResponse
from app.services.ai_service import generate_analysis_report

router = APIRouter(prefix="/api/v1", tags=["report"])


def _mock_result() -> dict:
    """AI 异常时的降级兜底结果，保证演示流程不中断。"""
    return {
        "summary": "（降级）AI 暂不可用，已按规则生成占位分析，待人工复核。",
        "personality_type": "老虎型",
        "personality_analysis": "（降级）该客户偏支配型，决策快、重结果。",
        "companion_advice": "（降级）沟通直接说结果，少铺垫。",
        "action_suggestions": "（降级）本周内安排一次产品演示，并给出明确报价。",
    }


@router.post(
    "/reports/analyze/{customer_id}",
    response_model=AnalysisReportResponse,
    status_code=201,
)
def analyze_customer(customer_id: int, db: Session = Depends(get_db)):
    """触发 AI 分析：读取客户聊天记录，调用大模型生成分析报告。"""
    if db.get(Customer, customer_id) is None:
        raise HTTPException(status_code=404, detail="客户不存在")

    # 拼接该客户的聊天记录作为分析输入
    chats = db.scalars(
        select(ChatRecord)
        .where(ChatRecord.customer_id == customer_id)
        .order_by(ChatRecord.id)
    ).all()
    if not chats:
        raise HTTPException(status_code=400, detail="该客户暂无聊天记录，无法分析")

    chat_text = "\n".join(c.content for c in chats)

    # 调用 AI 分析；异常则降级兜底，保证演示不中断
    try:
        raw = generate_analysis_report(chat_text)
        result = {
            "summary": raw.get("summary"),
            "personality_type": raw.get("personality_type"),
            "personality_analysis": raw.get("personality_analysis"),
            "companion_advice": raw.get("companion_advice"),
            "action_suggestions": raw.get("action_suggestions"),
        }
    except Exception:  # noqa: BLE001 - AI 异常走兜底
        result = _mock_result()

    # 版本号递增：取该客户已有报告的最大版本 +1
    max_version = db.scalar(
        select(func.max(AnalysisReport.version)).where(
            AnalysisReport.customer_id == customer_id
        )
    )
    next_version = (max_version or 0) + 1

    report = AnalysisReport(
        customer_id=customer_id,
        version=next_version,
        **result,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report
