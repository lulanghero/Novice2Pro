from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time

from core.orchestrator import run_agent
from config.settings import settings

app = FastAPI(title="RAG-LLM Agent Service")


# -----------------------------
# OpenAI 标准数据结构
# -----------------------------
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: float = 0.7
    stream: Optional[bool] = False  # ⚠️ 必须显式声明


# -----------------------------
# OpenAI Chat Completions 接口
# -----------------------------
@app.post("/v1/chat/completions")
def chat(
    req: ChatRequest,
    authorization: str = Header(None)
):
    # 1️⃣ 校验 API Key（Agent 自己的，不是 One-API 的）
    if not authorization or authorization != f"Bearer {settings.AGENT_API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 2️⃣ 校验模型名称
    if req.model != settings.AGENT_MODEL_NAME:
        raise HTTPException(status_code=400, detail="Invalid model name")

    # 3️⃣ 明确拒绝流式（避免 Chatbox 等 token）
    if req.stream:
        raise HTTPException(
            status_code=400,
            detail="Streaming is not supported by this model"
        )

    # 4️⃣ 提取 user 消息作为 query
    user_query = None
    for m in req.messages:
        if m.role == "user":
            user_query = m.content
            break

    if not user_query:
        raise HTTPException(status_code=400, detail="No user message found")

    # 5️⃣ 调用 Agent（RAG + LLM）
    try:
        answer_text = run_agent(user_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 6️⃣ 返回 OpenAI 标准响应
    return {
        "id": f"agent-{int(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": answer_text
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            # ⚠️ agent 内部真实 token 不可见，这里给 0 即可
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }
