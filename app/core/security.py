from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import API_TOKEN


security = HTTPBearer()


def verify_token(
    credentials: HTTPAuthorizationCredentials,
):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
        )

    return credentials