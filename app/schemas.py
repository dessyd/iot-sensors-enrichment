from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel


class DeviceCreate(BaseModel):
    device_id: str
    name: Optional[str] = None
    location: Optional[str] = None
    model: Optional[str] = None
    last_seen: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class DeviceRead(DeviceCreate):
    pass


class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: Optional[bool] = False


class UserRead(BaseModel):
    id: int
    username: str
    is_admin: bool


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
