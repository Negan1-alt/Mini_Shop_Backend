import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import JWT_ALGORITHM, JWT_SECRET

bearer = HTTPBearer()


def require_login(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {"id": int(payload["sub"]), "role": payload["role"]}
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="invalid or expired token")


def require_admin(user: dict = Depends(require_login)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="admin only")
    return user