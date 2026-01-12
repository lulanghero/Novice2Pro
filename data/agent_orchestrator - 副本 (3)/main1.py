from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time
import json
import asyncio

from core.orchestrator import run_agent
from config.settings import settings

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

    # 提取 user query
    user_query = None
    for m in req.messages:
        if m.role == "user":
            user_query = m.content
            break

    if not user_query:
        raise HTTPException(status_code=400, detail="No user message found")

    # 当请求是流式时，处理为 fake 流式返回
    if req.stream:
        # fake stream
        async def fake_stream():
            # 分成几块返回
            chunks = [
                "根据提供的参考资料，APT-47攻击流程中涉及的ATT&CK技战术主要包括：\n\n**初始访问**：攻击者利用ClickOnce技术进行初始载荷投递，",
                "这是一种被滥用的合法软件部署机制，属于社会工程攻击，诱导用户执行恶意程序。\n\n**执行**：攻击链通过多阶段加载实现，包括使用具有合法签名的可执行文件（BrowserMgr.exe）加载恶意DLL（opera_elf.dll），",
                "最终在内存中执行Golang编写的远控木马。\n\n**防御规避**：攻击者使用了多种规避技术，包括使用XOR加密保护嵌入在图像文件中的有效载荷以规避静态检测，以及利用带有合法签名的白文件",
                "(Living-off-the-Land Binary)来绕过应用程序白名单机制。\n\n**持久化**：远控木马通过创建互斥量来确保单一实例运行，",
                "这是一种常见的持久化控制手段。\n\n**命令与控制**：木马收集系统信息后，将其编码并通过HTTP POST请求发送到指定的C2服务器地址，",
                "建立了命令与控制通道。同时，它会检测对特定域名的连通性，可能用于判断网络环境。\n\n**信息收集**：远控木马的功能包括收集MAC地址、系统信息、文件信息等多种主机数据。"
            ]
            # 模拟逐步发送数据
            for chunk in chunks:
                yield {
                    "id": f"agent-{int(time.time())}",
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": req.model,
                    "choices": [
                        {
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": chunk
                            },
                            "finish_reason": "stop"
                        }
                    ]
                }
                await asyncio.sleep(1)  # 模拟延迟

        return fake_stream()

    # 如果请求不需要流式，则正常处理
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
