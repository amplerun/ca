from contextlib import asynccontextmanager
from typing import Any, Dict
import os
from fastapi import Depends, FastAPI, HTTPException, Request, status
from loguru import logger
from ruamel.yaml import YAML
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from ai_service.config import get_settings
from ai_service.middleware.auth import User, get_current_user
from ai_service.nodes import get_node
from ai_service.utils import YAMLResponse, create_error_response, logger as service_logger
from ai_service.models import __beanie_models__


settings = get_settings()
yaml = YAML(typ="safe")


@asynccontextmanager
async def lifespan(app: FastAPI):
    service_logger.info("AI Service starting up...")
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db_name = settings.MONGO_URI.split("/")[-1].split("?")[0]
    await init_beanie(database=client[db_name], document_models=__beanie_models__)
    service_logger.info(f"Beanie for AI Service initialized.")
    yield
    service_logger.info("AI Service shutting down.")


app = FastAPI(title="AIGIS AI Service", version="1.0.0", lifespan=lifespan, default_response_class=YAMLResponse)


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    corr_id = request.headers.get("X-Correlation-ID", "ai-local-" + os.urandom(4).hex())
    with service_logger.contextualize(correlation_id=corr_id):
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = corr_id
        return response


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "service": "ai-service"}


@app.post("/invoke/{node_name}", tags=["AI"])
async def invoke_node(
    node_name: str,
    request: Request,
    current_user: User = Depends(get_current_user),
):
    if request.headers.get("Content-Type") != "application/x-yaml":
        return create_error_response(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "INVALID_CONTENT_TYPE", "Unsupported media type.", "Content-Type must be application/x-yaml.")
    
    body = await request.body()
    try:
        payload: Dict[str, Any] = yaml.load(body.decode("utf-8"))
    except Exception as e:
        return create_error_response(status.HTTP_400_BAD_REQUEST, "INVALID_YAML", "Invalid YAML in request body.", str(e))

    try:
        node = get_node(node_name)
    except ValueError as e:
        return create_error_response(status.HTTP_404_NOT_FOUND, "NODE_NOT_FOUND", str(e), str(e))
        
    payload["user"] = current_user

    try:
        result_payload = await node.execute(payload)
        del result_payload["user"]
        return YAMLResponse(content={"status": "success", "data": result_payload})
    except Exception as e:
        logger.exception(f"Unhandled exception during node '{node_name}' execution.")
        return create_error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "INTERNAL_SERVER_ERROR", "An unexpected error occurred.", str(e))
