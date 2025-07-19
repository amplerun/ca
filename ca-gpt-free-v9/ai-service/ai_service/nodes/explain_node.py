import json
from typing import Any, Dict

from loguru import logger

from ai_service.nodes.base_node import BaseNode
from ai_service.services.prompt_loader import prompt_loader
from ai_service.utils import query_ollama
from ai_service.middleware.auth import User


class ExplainNode(BaseNode):
    """
    A node that takes structured data and generates a human-readable
    explanation using an LLM.
    """
    node_name = "ExplainNode"

    async def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        - Fetches the 'explain_generic' prompt.
        - Formats the input data as a string.
        - Queries the LLM to get an explanation.
        - Adds the explanation to the payload.
        """
        input_data = payload.get("input_data")
        current_user: User = payload.get("user")

        if not input_data or not current_user:
            raise ValueError("ExplainNode requires 'input_data' and 'user' in the payload.")

        prompt_template = await prompt_loader.get_prompt("explain_generic", current_user.companyId)
        if not prompt_template:
            raise ValueError("Could not load 'explain_generic' prompt from database.")

        system_message = "You are a helpful financial assistant. Explain the following data clearly and concisely in plain English. Your output must be a single JSON object with a key 'explanation'."
        
        # Convert the dict to a string for the prompt
        data_string = json.dumps(input_data, indent=2)
        
        full_prompt = prompt_template.format(data_to_explain=data_string)
        
        llm_response_str = await query_ollama(full_prompt, system_message)
        
        try:
            explanation_data = json.loads(llm_response_str)
            payload["explanation"] = explanation_data.get("explanation", "No explanation provided.")
            logger.info("Successfully generated explanation.")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON explanation from LLM response: {e}")
            logger.error(f"LLM Response was: {llm_response_str}")
            payload["explanation"] = f"Error processing AI response: {llm_response_str}"

        return payload