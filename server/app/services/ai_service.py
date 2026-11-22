"""AI 分析服务：调用大模型 API（OpenAI 兼容接口）生成客户分析报告。"""
import json

from app.core.config import settings

SYSTEM_PROMPT = """你是一个资深销售分析专家。
你需要判断客户的性格底色，只能从 DISC 模型的【老虎型(D)、孔雀型(I)、考拉型(S)、猫头鹰型(C)】中选一个，并给出分析。
你需要评估客户的 BANT 意向（预算 Budget、决策权 Authority、需求 Need、时间 Timeline）。
你必须给出具体的"陪伴建议"和"下一步行动建议"。
请只返回一个 JSON 对象，不要输出任何其他文字，字段如下：
{
  "summary": "客户分析摘要（含 BANT 意向概述）",
  "personality_type": "老虎型/孔雀型/考拉型/猫头鹰型 之一",
  "personality_analysis": "基于 DISC 的性格行为解读",
  "companion_advice": "陪伴建议（针对该性格的沟通策略）",
  "action_suggestions": "下一步行动建议（基于 BANT 和 DISC）"
}"""


def _parse_json(content: str) -> dict:
    """从模型返回内容中解析 JSON，兼容 markdown 代码块包裹。"""
    content = content.strip()
    if content.startswith("```"):
        content = content.strip("`")
        if content.lower().startswith("json"):
            content = content[4:]
        content = content.strip()
    return json.loads(content)


def generate_analysis_report(chat_text: str) -> dict:
    """调用大模型 API，根据聊天文本生成分析报告，返回对齐 AnalysisReport 字段的 dict。"""
    import httpx  # 延迟导入，避免未安装 httpx 时影响应用启动

    payload = {
        "model": settings.AI_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": chat_text},
        ],
        "temperature": 0.3,
    }
    headers = {
        "Authorization": f"Bearer {settings.AI_API_KEY}",
        "Content-Type": "application/json",
    }

    with httpx.Client(timeout=60.0) as client:
        resp = client.post(settings.AI_BASE_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    content = data["choices"][0]["message"]["content"]
    return _parse_json(content)
