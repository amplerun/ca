import json
from typing import Any, Dict
from beanie import PydanticObjectId
from ai_service.nodes.base_node import BaseNode
from ai_service.services.prompt_loader import prompt_loader
from ai_service.utils import query_ollama
from ai_service.middleware.auth import User

class YamlCleanNode(BaseNode):
    node_name = "YamlCleanNode"

    async def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = payload.get("raw_text")
        current_user: User = payload.get("user")
        if not raw_text or not current_user:
            raise ValueError("YamlCleanNode requires 'raw_text' and 'user' in payload.")
        
        prompt_template = await prompt_loader.get_prompt("clean_invoice", PydanticObjectId(current_user.companyId))
        if not prompt_template:
            raise ValueError("Could not load 'clean_invoice' prompt.")
        
        system_message = "You are a data extraction assistant. Your only output should be valid JSON as requested."
        full_prompt = prompt_template.format(invoice_data=raw_text)
        
        llm_response_str = await query_ollama(full_prompt, system_message)

        try:
            cleaned_data = json.loads(llm_response_str)
            payload["cleaned_data"] = cleaned_data
        except json.JSONDecodeError:
            raise ValueError(f"AI model returned malformed data: {llm_response_str}")

        return payload
