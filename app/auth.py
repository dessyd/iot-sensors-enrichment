import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app import crud
from app.db import get_session
from app.models import User


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/auth/token")

JWT_SECRET = os.environ.get("JWT_SECRET", "change-this-secret")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
JWT_EXP_MINUTES = int(os.environ.get("JWT_EXPIRATION", "60"))


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain password against the hashed value."""
    return PWD_CONTEXT.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    """Hash a password for storage."""
    return PWD_CONTEXT.hash(password)


def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token containing "sub" and "exp"."""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire_dt = now + (expires_delta or timedelta(minutes=JWT_EXP_MINUTES))
    # JWT exp should be a numeric timestamp
    to_encode.update({"exp": int(expire_dt.timestamp())})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


async def get_current_user(
    token: str = Depends(OAUTH2_SCHEME), session: Session = Depends(get_session)
) -> User:
    """Dependency that returns the currently authenticated user."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = crud.get_user_by_username(session, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


async def require_admin(current_user: User = Depends(get_current_user)) -> None:
    """Ensure the current user has admin privileges."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required"
        )

