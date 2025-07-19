import time
from typing import Dict, Any, Optional
from beanie import PydanticObjectId
from loguru import logger
from ai_service.config import get_settings
from ai_service.models.prompt import Prompt

settings = get_settings()

class PromptLoader:
    _instance = None
    _prompt_cache: Dict[str, Dict[str, Any]] = {}
    _last_load_time: Dict[str, float] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PromptLoader, cls).__new__(cls)
        return cls._instance

    async def get_prompt(self, prompt_name: str, company_id: PydanticObjectId) -> Optional[str]:
        cache_key = f"{str(company_id)}:{prompt_name}"
        current_time = time.time()

        if cache_key in self._prompt_cache and (current_time - self._last_load_time.get(cache_key, 0)) < settings.PROMPT_CACHE_TTL_SECONDS:
            return self._prompt_cache[cache_key]["text"]
        
        prompt_doc = await Prompt.find_one({"name": prompt_name, "companyId": company_id})
        if not prompt_doc:
            prompt_doc = await Prompt.find_one({"name": prompt_name, "companyId": None})

        if prompt_doc:
            self._prompt_cache[cache_key] = {"text": prompt_doc.text}
            self._last_load_time[cache_key] = current_time
            return prompt_doc.text
        
        logger.error(f"Prompt '{prompt_name}' not found for company '{company_id}' or as a default.")
        return None

prompt_loader = PromptLoader()
