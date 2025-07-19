import json
from typing import Any, Dict
from loguru import logger
from ai_service.nodes.base_node import BaseNode
from ai_service.utils import query_ollama
from ai_service.middleware.auth import User

class ChatNode(BaseNode):
    node_name = "ChatNode"

    async def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        user_message: str = payload.get("message")
        if not user_message:
            raise ValueError("ChatNode requires 'message' in the payload.")
        
        system_message = "You are a helpful assistant."
        llm_response_str = await query_ollama(user_message, system_message)
        
        try:
            response_data = json.loads(llm_response_str)
            ai_response = response_data.get("response", llm_response_str)
        except json.JSONDecodeError:
            ai_response = llm_response_str
        
        payload["response"] = ai_response.strip()
        return payload
