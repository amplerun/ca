import json
from typing import Any, Dict, List

from loguru import logger

from ai_service.nodes.base_node import BaseNode
from ai_service.utils import query_ollama
from ai_service.middleware.auth import User

class ChatNode(BaseNode):
    """
    A node for handling conversational chat interactions.
    """
    node_name = "ChatNode"

    async def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        - Takes a history of messages and a new user message.
        - Queries the LLM for a conversational response.
        """
        history: List[Dict[str, str]] = payload.get("history", [])
        user_message: str = payload.get("message")
        current_user: User = payload.get("user")

        if not user_message or not current_user:
            raise ValueError("ChatNode requires 'message' and 'user' in the payload.")

        # For a simple chat, we can use a generic system prompt.
        # More advanced versions could load this from the DB.
        system_message = "You are a helpful assistant for a Chartered Accountancy firm. Answer the user's questions clearly and professionally."
        
        # Ollama's `generate` endpoint is stateless, so we just send the latest prompt.
        # For true conversational context, one would use the `/api/chat` endpoint and manage context,
        # but for this simple implementation, we'll just use the last message.
        
        # A more complete implementation would be:
        # full_prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
        # full_prompt += f"\nuser: {user_message}"
        
        llm_response_str = await query_ollama(user_message, system_message)
        
        try:
            # Assuming the model might still wrap its simple chat in JSON.
            # If not, we handle the raw string.
            response_data = json.loads(llm_response_str)
            ai_response = response_data.get("response", llm_response_str)
        except json.JSONDecodeError:
            # The response was not a JSON object, so use it as a raw string.
            ai_response = llm_response_str
        
        payload["response"] = ai_response.strip()
        logger.info("Successfully generated chat response.")
        
        return payload