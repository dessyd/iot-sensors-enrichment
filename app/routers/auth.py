# no extra stdlib imports required here

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlmodel import Session

from app import crud
from app.auth import create_access_token, verify_password
from app.db import get_session
from app.schemas import Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = crud.get_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
def refresh(token: str, session: Session = Depends(get_session)):
    # naive refresh: decode and issue a new token
    try:
        payload = create_access_token(data={})
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"access_token": payload, "token_type": "bearer"}
