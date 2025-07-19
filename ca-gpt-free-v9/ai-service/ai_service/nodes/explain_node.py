import json
from typing import Any, Dict
from beanie import PydanticObjectId
from ai_service.nodes.base_node import BaseNode
from ai_service.services.prompt_loader import prompt_loader
from ai_service.utils import query_ollama
from ai_service.middleware.auth import User

class ExplainNode(BaseNode):
    node_name = "ExplainNode"

    async def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        input_data = payload.get("input_data")
        current_user: User = payload.get("user")
        if not input_data or not current_user:
            raise ValueError("ExplainNode requires 'input_data' and 'user' in payload.")

        prompt_template = await prompt_loader.get_prompt("explain_generic", PydanticObjectId(current_user.companyId))
        if not prompt_template:
            raise ValueError("Could not load 'explain_generic' prompt.")

        system_message = "You are a helpful financial assistant. Your output must be a single JSON object with a key 'explanation'."
        data_string = json.dumps(input_data, indent=2)
        full_prompt = prompt_template.format(data_to_explain=data_string)
        
        llm_response_str = await query_ollama(full_prompt, system_message)
        
        try:
            explanation_data = json.loads(llm_response_str)
            payload["explanation"] = explanation_data.get("explanation", "No explanation provided.")
        except json.JSONDecodeError:
            payload["explanation"] = f"Error: AI returned malformed data: {llm_response_str}"

        return payload
