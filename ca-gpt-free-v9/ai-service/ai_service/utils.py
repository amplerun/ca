import sys
from typing import Any
import httpx
from fastapi import HTTPException, Response
from loguru import logger
from ruamel.yaml import YAML
from tenacity import retry, stop_after_attempt, wait_exponential
from ai_service.config import get_settings

settings = get_settings()
logger.remove()
logger.add(sys.stderr, format="{time} {level} {extra[correlation_id]} | {message}", level=settings.LOG_LEVEL)
yaml = YAML(typ="safe")
yaml.default_flow_style = False

class YAMLResponse(Response):
    media_type = "application/x-yaml"
    def render(self, content: Any) -> bytes:
        from io import StringIO
        string_stream = StringIO()
        yaml.dump(content, string_stream)
        return string_stream.getvalue().encode("utf-8")

def create_error_response(status_code: int, code: str, user_message: str, dev_message: str) -> YAMLResponse:
    return YAMLResponse(content={"status": "error", "code": code, "userMessage": user_message, "devMessage": dev_message}, status_code=status_code)

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
async def query_ollama(prompt: str, system_message: str) -> str:
    url = f"{settings.OLLAMA_HOST}/api/generate"
    payload = {"model": settings.OLLAMA_MODEL, "prompt": prompt, "system": system_message, "stream": False, "format": "json"}
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            import json
            json_objects = [json.loads(line) for line in response.text.strip().split('\n') if line]
            final_response = json_objects[-1]
            if final_response.get("done"):
                return final_response.get("response", "")
            else:
                raise httpx.HTTPError("Incomplete response from Ollama")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail="Could not connect to the AI service (Ollama).")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred with the AI service: {e}")
