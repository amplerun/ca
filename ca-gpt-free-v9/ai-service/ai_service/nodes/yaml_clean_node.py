import json
from typing import Any, Dict

from loguru import logger

from ai_service.nodes.base_node import BaseNode
from ai_service.services.prompt_loader import prompt_loader
from ai_service.utils import query_ollama
from ai_service.middleware.auth import User

class YamlCleanNode(BaseNode):
    """
    A node that takes messy text input (e.g., from OCR) and uses an LLM
    to clean it and structure it as YAML according to a prompt.
    """
    node_name = "YamlCleanNode"

    async def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        - Fetches the 'clean_invoice' prompt.
        - Queries the LLM with the raw text.
        - Parses the LLM's YAML output and adds it to the payload.
        """
        raw_text = payload.get("raw_text")
        current_user: User = payload.get("user")

        if not raw_text or not current_user:
            raise ValueError("YamlCleanNode requires 'raw_text' and 'user' in the payload.")
        
        prompt_template = await prompt_loader.get_prompt("clean_invoice", current_user.companyId)
        if not prompt_template:
            raise ValueError("Could not load 'clean_invoice' prompt from database.")
        
        # We don't use a system message here, as the full instruction is in the prompt
        system_message = "You are a data extraction assistant. Your only output should be valid JSON as requested in the user prompt."
        
        # The prompt is a template expecting the raw text
        full_prompt = prompt_template.format(invoice_data=raw_text)
        
        llm_response_str = await query_ollama(full_prompt, system_message)

        try:
            # The LLM should return a JSON string, which we parse.
            cleaned_data = json.loads(llm_response_str)
            logger.info("Successfully parsed cleaned data from LLM response.")
            payload["cleaned_data"] = cleaned_data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from LLM response: {e}")
            logger.error(f"LLM Response was: {llm_response_str}")
            raise ValueError(f"AI model returned malformed data. Raw output: {llm_response_str}")

        return payload