from typing import Optional, List, Dict, Any
from fastapi import Depends, HTTPException, Request, status
import jwt
from pydantic import BaseModel, ValidationError

from ai_service.config import get_settings
from ai_service.utils import create_error_response

settings = get_settings()

class User(BaseModel):
    id: str
    companyId: str
    email: str
    permissions: List[str]

def get_current_user(request: Request) -> User:
    """
    Dependency to decode JWT from Authorization header and return user data.
    """
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
            response=create_error_response(
                status.HTTP_401_UNAUTHORIZED,
                "AUTH_HEADER_MISSING",
                "Authentication required.",
                "Authorization header is missing.",
            ),
        )

    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_data = {
            "id": payload.get("id"),
            "companyId": payload.get("companyId"),
            "email": payload.get("email"),
            "permissions": payload.get("permissions", [])
        }
        return User(**user_data)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            response=create_error_response(
                status.HTTP_401_UNAUTHORIZED,
                "TOKEN_EXPIRED",
                "Your session has expired. Please log in again.",
                "JWT has expired.",
            ),
        )
    except (jwt.PyJWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
            response=create_error_response(
                status.HTTP_401_UNAUTHORIZED,
                "INVALID_TOKEN",
                "Your session is invalid. Please log in again.",
                f"Could not validate credentials: {e}",
            ),
        )

def require_permission(required_permission: str):
    """
    Dependency factory to check if the current user has a specific permission.
    """
    def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if required_permission not in current_user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                response=create_error_response(
                    status.HTTP_403_FORBIDDEN,
                    "INSUFFICIENT_PERMISSIONS",
                    "You do not have permission to perform this action.",
                    f"User lacks required permission: '{required_permission}'.",
                ),
            )
        return current_user
    return permission_checker