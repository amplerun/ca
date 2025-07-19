from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import Depends, FastAPI, HTTPException, Request, status
from loguru import logger
from ruamel.yaml import YAML

from ai_service.config import get_settings
from ai_service.middleware.auth import User, get_current_user
from ai_service.nodes import get_node
from ai_service.utils import YAMLResponse, create_error_response, logger as service_logger

# Initialize settings and YAML parser
settings = get_settings()
yaml = YAML(typ="safe")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # This block runs on startup
    service_logger.info("AI Service starting up...")
    # Pre-warm the prompt loader cache (optional, but good practice)
    from ai_service.services.prompt_loader import prompt_loader
    # You could add a call here to load critical prompts if needed
    service_logger.info("AI Service startup complete.")
    yield
    # This block runs on shutdown
    service_logger.info("AI Service shutting down.")


app = FastAPI(
    title="AIGIS AI Service",
    version="1.0.0",
    lifespan=lifespan,
    default_response_class=YAMLResponse,
)


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    # Get correlation ID from header or generate a new one
    corr_id = request.headers.get("X-Correlation-ID", "ai-local-" + os.urandom(4).hex())
    # Add it to the logger's context
    with service_logger.contextualize(correlation_id=corr_id):
        response = await call_next(request)
        # Add the correlation ID to the response headers
        response.headers["X-Correlation-ID"] = corr_id
        return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Use our custom YAML error response for FastAPI's built-in exceptions
    if isinstance(exc.detail, dict) and "code" in exc.detail: # Our custom errors
        return exc.response
    return create_error_response(
        status_code=exc.status_code,
        code="HTTP_EXCEPTION",
        user_message=str(exc.detail),
        dev_message=str(exc.detail),
    )

@app.get("/health", tags=["System"], response_class=YAMLResponse)
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "ai-service"}


@app.post("/invoke/{node_name}", tags=["AI"], response_class=YAMLResponse)
async def invoke_node(
    node_name: str,
    request: Request,
    current_user: User = Depends(get_current_user),
):
    """
    Dynamically invokes a processing node from the PocketFlow registry.
    The request body is passed as the initial payload to the node.
    """
    try:
        if request.headers.get("Content-Type") != "application/x-yaml":
            return create_error_response(
                status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                "INVALID_CONTENT_TYPE",
                "Unsupported media type. Please use application/x-yaml.",
                "Content-Type header must be application/x-yaml.",
            )
        
        body = await request.body()
        payload: Dict[str, Any] = yaml.load(body.decode("utf-8"))
    except Exception as e:
        return create_error_response(
            status.HTTP_400_BAD_REQUEST,
            "INVALID_YAML",
            "The provided request body is not valid YAML.",
            f"YAML parsing error: {e}",
        )
    
    try:
        node = get_node(node_name)
    except ValueError as e:
        return create_error_response(
            status.HTTP_404_NOT_FOUND, "NODE_NOT_FOUND", str(e), str(e)
        )
        
    # Inject user into the payload for the node to use
    payload["user"] = current_user

    try:
        result_payload = await node.execute(payload)
        # Remove user object before sending response
        del result_payload["user"]
        return YAMLResponse(content={"status": "success", "data": result_payload})
    except ValueError as e:
        return create_error_response(
            status.HTTP_400_BAD_REQUEST, "NODE_EXECUTION_ERROR", str(e), str(e)
        )
    except Exception as e:
        logger.exception(f"Unhandled exception during node '{node_name}' execution.")
        return create_error_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "INTERNAL_SERVER_ERROR",
            "An unexpected error occurred while processing your request.",
            str(e),
        )