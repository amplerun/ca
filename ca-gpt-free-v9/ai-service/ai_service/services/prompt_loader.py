import asyncio
from typing import Dict, Optional, Any
from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorClient
from loguru import logger
import time

from ai_service.config import get_settings

settings = get_settings()

class PromptLoader:
    _instance = None
    _db = None
    _prompt_cache: Dict[str, Dict[str, Any]] = {}
    _last_load_time: Dict[str, float] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PromptLoader, cls).__new__(cls)
            client = AsyncIOMotorClient(settings.MONGO_URI)
            cls._db = client.get_database() # The DB name is part of the URI
        return cls._instance

    async def get_prompt(self, prompt_name: str, company_id: str) -> Optional[str]:
        """
        Retrieves a prompt for a given company.
        First checks the cache. If stale or not found, reloads from DB.
        Falls back to a global default prompt if a company-specific one isn't found.
        """
        cache_key = f"{company_id}:{prompt_name}"
        current_time = time.time()

        if (
            cache_key in self._prompt_cache and
            (current_time - self._last_load_time.get(cache_key, 0)) < settings.PROMPT_CACHE_TTL_SECONDS
        ):
            logger.debug(f"Returning cached prompt for '{cache_key}'")
            return self._prompt_cache[cache_key]["text"]
        
        logger.info(f"Cache miss or stale for prompt '{cache_key}'. Fetching from DB.")
        
        # Try to find a company-specific prompt first
        prompt_doc = await self._db.prompts.find_one(
            {"name": prompt_name, "companyId": company_id}
        )

        # If not found, fall back to the global default prompt (companyId is null)
        if not prompt_doc:
            logger.warning(f"No company-specific prompt '{prompt_name}' for company '{company_id}'. Falling back to default.")
            prompt_doc = await self._db.prompts.find_one(
                {"name": prompt_name, "companyId": None}
            )

        if prompt_doc:
            self._prompt_cache[cache_key] = {
                "text": prompt_doc["text"],
                "version": prompt_doc.get("__v", 0)
            }
            self._last_load_time[cache_key] = current_time
            logger.success(f"Successfully loaded and cached prompt '{cache_key}'.")
            return prompt_doc["text"]
        
        logger.error(f"Prompt '{prompt_name}' not found for company '{company_id}' or as a global default.")
        return None

# Singleton instance
prompt_loader = PromptLoader()