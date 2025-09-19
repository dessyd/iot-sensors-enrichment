from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field, Column, JSON
from datetime import datetime


class Device(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    device_id: str = Field(index=True, nullable=False)
    name: Optional[str] = None
    location: Optional[str] = None
    model: Optional[str] = None
    last_seen: Optional[datetime] = None
    # `metadata` is a reserved attribute name on SQLAlchemy declarative
    # so use `metadata_` as the Python attribute while keeping the
    # underlying column name `metadata` in the database.
    metadata_: Optional[Dict[str, Any]] = Field(
        default=None, sa_column=Column("metadata", JSON)
    )


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False, unique=True)
    hashed_password: str
    is_admin: bool = Field(default=False)
