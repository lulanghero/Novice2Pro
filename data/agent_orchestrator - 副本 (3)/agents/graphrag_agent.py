import requests
import json


class GraphRAGAgent:
    """
        原有能力：GraphRAG 作为 LLM 直接生成答案
        ⚠️ 不推荐用于 Agent 主流程，但保留
    """
    def __init__(self):
        self.url = "http://localhost:8012/v1/chat/completions"

    def run(self, query: str) -> str:  # 改成同步 def
        payload = {
            "model": "full-model:latest",
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ],
            "temperature": 0.7
        }

        headers = {
            "Content-Type": "application/json"
        }

        # ⚠️ 用 requests，不用 httpx
        resp = requests.post(
            self.url,
            headers=headers,
            data=json.dumps(payload),
            timeout=180
        )

        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


class GraphRAGSearchAgent:
    """
        新增能力：
        - GraphRAG 只负责【检索 + 结构化摘要】
        - 输出作为 Agent Context
    """
    def __init__(self):
        self.url = "http://localhost:8012/v1/chat/completions"

    def search(self, query: str) -> str:  # ❌ 不用 async
        payload = {
             "model": "graphrag-local-search:latest",
             "messages": [
                {
                     "role": "user",
                     "content": (
                         "请基于图数据库检索与问题高度相关的事实、实体与关系，"
                         "以【参考资料】形式返回，不要做结论性回答。\n\n"
                         f"问题：{query}"
                     )
                }
                ],
             "temperature": 0.0
            }

        headers = {"Content-Type": "application/json"}

        resp = requests.post(
            self.url,
            headers=headers,
            data=json.dumps(payload),
            timeout=180
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
