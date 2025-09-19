from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session

from app.db import get_session, init_db
from app.auth import get_password_hash, require_admin, get_current_user
from app import crud
from app.models import User
from app.schemas import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=201)
def create_user(
    payload: UserCreate,
    session: Session = Depends(get_session),
    _=Depends(require_admin),
):
    existing = crud.get_user_by_username(session, payload.username)
    if existing:
        raise HTTPException(status_code=409, detail="User already exists")
    user = User(
        username=payload.username,
        hashed_password=get_password_hash(payload.password),
        is_admin=payload.is_admin,
    )
    return crud.create_user(session, user)


@router.get("", response_model=List[UserRead])
def list_users(session: Session = Depends(get_session), _=Depends(require_admin)):
    return crud.list_users(session)


@router.get("/{username}", response_model=UserRead)
def get_user(
    username: str,
    session: Session = Depends(get_session),
    _=Depends(require_admin),
):
    user = crud.get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead(id=user.id, username=user.username, is_admin=user.is_admin)


@router.delete("/{username}", status_code=204)
def delete_user(
    username: str,
    session: Session = Depends(get_session),
    _=Depends(require_admin),
):
    user = crud.get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.username == "admin":
        raise HTTPException(status_code=400, detail="Cannot delete admin")
    crud.delete_user(session, user)
    return {}
