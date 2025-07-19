from typing import List
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
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing or invalid.")
    token = token.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return User(**payload)
    except (jwt.PyJWTError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials: {e}")
