import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str
    JWT_SECRET: str
    OLLAMA_HOST: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "mistral"
    PROMPT_CACHE_TTL_SECONDS: int = 900  # 15 minutes
    PORT: int = 8001
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    # Validate required environment variables on startup
    required_vars = ["MONGO_URI", "JWT_SECRET", "OLLAMA_HOST", "OLLAMA_MODEL"]
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"Missing required environment variable: {var}")
    return Settings()