from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from .config import settings

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(username: str, user_id: int, role:str, expires_delta: timedelta):
    encode = {
        "sub": username,
        "id": user_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(encode, settings.secret_key, algorithm=settings.algorithm)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        if not username or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No validation")
        return {"username": username, "id": user_id, "role": role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No validation")
