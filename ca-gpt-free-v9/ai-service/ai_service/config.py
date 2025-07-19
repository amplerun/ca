import os
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str
    JWT_SECRET: str
    OLLAMA_HOST: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "mistral"
    PROMPT_CACHE_TTL_SECONDS: int = 900
    LOG_LEVEL: str = "INFO"

@lru_cache()
def get_settings() -> Settings:
    for var in ["MONGO_URI", "JWT_SECRET", "OLLAMA_HOST"]:
        if not os.getenv(var):
            raise ValueError(f"Missing required environment variable: {var}")
    return Settings()
