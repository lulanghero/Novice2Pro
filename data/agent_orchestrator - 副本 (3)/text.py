import requests

# 🌟 修改为你的本地服务 URL
AGENT_URL = "http://127.0.0.1:8000/v1/chat/completions"

# 🌟 从 .env 拿到的 Agent API Key
AGENT_API_KEY = "lysh20030530."

# 🌟 模型名称，必须和 settings.AGTENT_MODEL_NAME 一致
MODEL_NAME = "apt-killer-v1"

# 测试问题
query = "请结合 MITRE ATT&CK 框架的技战术分类，分析上述 APT-47 攻击流程中包含了哪些具体的 ATT&CK 技战术？"

# 构建消息列表（OpenAI Chat 格式）
messages = [
    {"role": "user", "content": query}
]

payload = {
    "model": MODEL_NAME,
    "messages": messages,
    "temperature": 0.7
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AGENT_API_KEY}"
}

# 调用 Agent 服务
resp = requests.post(AGENT_URL, headers=headers, json=payload)
resp.raise_for_status()

# 输出完整 JSON
data = resp.json()
print("Full response JSON:\n", data)

# 输出 assistant 消息
assistant_msg = data["choices"][0]["message"]["content"]
print("\nAssistant response:\n", assistant_msg)
