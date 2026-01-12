from agents.graphrag_agent import GraphRAGSearchAgent
from config.settings import settings
import requests
import os
from typing import TypedDict, List, Dict


class AgentResult(TypedDict):
    messages: List[Dict[str, str]]
    summary: str


# -----------------------------
# 读取 summarize.txt 提示词
# -----------------------------
PROMPT_FILE = os.path.join(os.path.dirname(__file__), "../prompts/summarize.txt")
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    AGENT_PROMPT = f.read().strip()


# -----------------------------
# 主调度函数（核心）
# -----------------------------
def run_agent(query: str) -> AgentResult:
    # 1️⃣ GraphRAG 检索
    search_agent = GraphRAGSearchAgent()
    context = search_agent.search(query)

    # 2️⃣ 构造给 LLM 的 messages
    messages = [
        {"role": "system", "content": AGENT_PROMPT},
        {"role": "user", "content": query},
        {"role": "assistant", "content": "【参考资料】\n" + context},
    ]

    # 3️⃣ 调用 One-API LLM
    payload = {
        "model": settings.ONE_API_CHAT_MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.ONE_API_KEY}"
    }

    resp = requests.post(
        f"{settings.ONE_API_BASE}/chat/completions",
        headers=headers,
        json=payload,
        timeout=180
    )
    resp.raise_for_status()

    data = resp.json()

    # 4️⃣ 取出 LLM 输出（⚠️ 之前你漏了这一步）
    llm_output: str = data["choices"][0]["message"]["content"]

    # 5️⃣ 返回 Agent 结构化结果
    return {
        "messages": messages,
        "summary": llm_output
    }
