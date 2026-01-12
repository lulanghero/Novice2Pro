from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GRAPHRAG_SERVER: str = "http://localhost:8012"

    # 新增 One-API LLM 配置
    ONE_API_BASE: str
    ONE_API_KEY: str
    ONE_API_CHAT_MODEL: str

    # 新增openai接口调用的校验信息
    AGENT_API_KEY: str
    AGENT_MODEL_NAME: str

    class Config:
        env_file = ".env"
        # 新增
        env_file_encoding = "utf-8"
        # ⚠️ 如果有 extra fields 报错，可以加：
        extra = "forbid"  # 默认
        # extra = "allow"  # 临时跳过未知字段

settings = Settings()
