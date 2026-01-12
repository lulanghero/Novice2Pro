from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time
import json
import asyncio
from core.orchestrator import run_agent
from config.settings import settings
from fastapi.responses import StreamingResponse

app = FastAPI(
    title="RAG-LLM Agent Service",
    version="1.0.0"
)

# =====================================================
# OpenAI 标准数据结构
# =====================================================
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: float = 0.7
    stream: Optional[bool] = False   # Chatbox / Cherry 会传


# =====================================================
# 通用校验函数（不动你原有规则）
# =====================================================

def verify_api_key(authorization: Optional[str]):
    if not authorization or authorization != f"Bearer {settings.AGENT_API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")


def verify_model_name(model: str):
    if model != settings.AGENT_MODEL_NAME:
        raise HTTPException(status_code=400, detail="Invalid model name")


# =====================================================
# 1️⃣ Models 接口（UI 能否识别你的关键）
# =====================================================

@app.get("/v1/models")
def list_models(authorization: str = Header(None)):
    verify_api_key(authorization)

    return {
        "object": "list",
        "data": [
            {
                "id": settings.AGENT_MODEL_NAME,
                "object": "model",
                "owned_by": "agent",
                "permission": []
            }
        ]
    }


# =====================================================
# 2️⃣ Chat Completions（核心接口）
# =====================================================

@app.post("/v1/chat/completions")
async def chat_completions(
    req: ChatRequest,
    authorization: str = Header(None)
):
    # 校验
    verify_api_key(authorization)
    verify_model_name(req.model)

    # 明确拒绝流式（但方式要“协议友好”）
    if req.stream:
        # 流式数据
        async def event_generator():
            # 提取 user query
            user_query = None
            for m in req.messages:
                if m.role == "user":
                    user_query = m.content
                    break

            if not user_query:
                raise HTTPException(status_code=400, detail="No user message found")

            # 调用 Agent（RAG + 内部 LLM）
            try:
                agent_result = run_agent(user_query)
                text = agent_result["summary"]
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

            # 模拟逐 token 输出（按句子/字符都行）
            for ch in text:
                chunk = {
                    "id": f"agent-{int(time.time())}",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": req.model,
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"content": ch},
                            "finish_reason": None
                        }
                    ]
                }
                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
                await asyncio.sleep(0.01)  # 控制“打字速度”

            # 结束信号（非常重要）
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream"
        )

    # 如果不是流式，正常返回（非流式）
    user_query = next((m.content for m in req.messages if m.role == "user"), None)
    if not user_query:
        raise HTTPException(status_code=400, detail="No user message found")

    # 调用 Agent（RAG + 内部 LLM）
    try:
        agent_result = run_agent(user_query)
        answer_text = agent_result["summary"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    now = int(time.time())

    return {
        "id": f"agent-{now}",
        "object": "chat.completion",
        "created": now,
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
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }


# =====================================================
# 3️⃣ Completions（老客户端兜底）
# =====================================================

class CompletionRequest(BaseModel):
    model: str
    prompt: str
    temperature: float = 0.7


@app.post("/v1/completions")
def completions(
    req: CompletionRequest,
    authorization: str = Header(None)
):
    verify_api_key(authorization)
    verify_model_name(req.model)

    try:
        agent_result = run_agent(req.prompt)
        text = agent_result["summary"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    now = int(time.time())

    return {
        "id": f"agent-{now}",
        "object": "text_completion",
        "created": now,
        "model": req.model,
        "choices": [
            {
                "text": text,
                "index": 0,
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }


# =====================================================
# 4️⃣ Health（部分 UI 会 probe）
# =====================================================

@app.get("/health")
def health():
    return {"status": "ok"}
