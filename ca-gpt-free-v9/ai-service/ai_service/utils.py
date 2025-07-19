import sys
from typing import Any, Dict

import httpx
from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse
from loguru import logger
from ruamel.yaml import YAML
from tenacity import retry, stop_after_attempt, wait_exponential

from ai_service.config import get_settings

settings = get_settings()

# Configure logger
logger.remove()
logger.add(
    sys.stderr,
    format="{time} {level} {extra[correlation_id]} | {message}",
    level=settings.LOG_LEVEL,
)

yaml = YAML(typ="safe")
yaml.default_flow_style = False


class YAMLResponse(Response):
    media_type = "application/x-yaml"

    def render(self, content: Any) -> bytes:
        from io import StringIO
        string_stream = StringIO()
        yaml.dump(content, string_stream)
        return string_stream.getvalue().encode("utf-8")


def create_error_response(
    status_code: int, code: str, user_message: str, dev_message: str
) -> YAMLResponse:
    content = {
        "status": "error",
        "code": code,
        "userMessage": user_message,
        "devMessage": dev_message,
    }
    return YAMLResponse(content=content, status_code=status_code)


@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
async def query_ollama(prompt: str, system_message: str) -> str:
    """
    Queries the Ollama service with retry logic.
    """
    url = f"{settings.OLLAMA_HOST}/api/generate"
    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": prompt,
        "system": system_message,
        "stream": False,
        "format": "json" # We ask for JSON output for easier parsing
    }
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            logger.info(f"Querying Ollama model '{settings.OLLAMA_MODEL}'...")
            response = await client.post(url, json=payload)
            response.raise_for_status()
            
            # The response from Ollama is a stream of JSON objects, even with stream=false
            # We need to piece them together.
            full_response_text = response.text
            import json
            
            # Ollama returns multiple JSON objects on one line, we just need the last one
            # for the full response.
            json_objects = [json.loads(line) for line in full_response_text.strip().split('\n') if line]
            final_response_part = json_objects[-1]

            if final_response_part.get("done"):
                logger.success("Successfully received response from Ollama.")
                return final_response_part.get("response", "")
            else:
                logger.warning("Ollama response indicates process is not done. Retrying...")
                raise httpx.HTTPError("Incomplete response from Ollama")

    except httpx.RequestError as e:
        logger.error(f"Error connecting to Ollama: {e}")
        raise HTTPException(
            status_code=503,
            detail="Could not connect to the AI service (Ollama). Please try again later.",
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred while querying Ollama: {e}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred with the AI service."
        )