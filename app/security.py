import os

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

JWT_SECRET = os.getenv("JWT_SECRET", "dev")  # для учебных задач
bearer = HTTPBearer(auto_error=False)


def require_jwt(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    if creds is None:
        raise HTTPException(status_code=401, detail="missing credentials")
    try:
        jwt.decode(creds.credentials, JWT_SECRET, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=401, detail="invalid token")


def assert_secure_config():
    env = os.getenv("ENV", "dev").lower()
    if env == "prod" and JWT_SECRET == "dev":
        raise RuntimeError("insecure configuration")
