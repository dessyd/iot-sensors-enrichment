import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool

# ensure project root on path before importing app
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import app as fastapi_app  # noqa: E402


@pytest.fixture(scope="session")
def engine():
    # in-memory sqlite for tests
    # Use a StaticPool so multiple connections (and threads) share the same
    # in-memory SQLite database for the duration of the tests.
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture()
def session(engine):
    with Session(engine) as s:
        yield s


@pytest.fixture()
def client(engine, session, monkeypatch):
    # override get_session dependency
    def get_session_override():
        with Session(engine) as s:
            yield s

    # Use FastAPI's dependency_overrides so the router dependencies call
    # our in-memory session provider (monkeypatching the module name is
    # insufficient because FastAPI captures the callable at import time).
    from app.db import get_session as real_get_session

    fastapi_app.dependency_overrides[real_get_session] = get_session_override

    # ensure ADMIN_PASSWORD is set so lifespan init creates admin user
    os.environ.setdefault("ADMIN_PASSWORD", "testadmin")

    # Also ensure an admin user exists in the in-memory engine used for tests.
    # The app's lifespan init writes to the file-backed engine; tests use an
    # in-memory engine, so create the admin here if missing.
    from app.auth import get_password_hash
    from app.crud import get_user_by_username, create_user
    from app.models import User

    admin_pw = os.environ.get("ADMIN_PASSWORD", "testadmin")
    with Session(engine) as s:
        if not get_user_by_username(s, "admin"):
            user = User(
                username="admin",
                hashed_password=get_password_hash(admin_pw),
                is_admin=True,
            )
            create_user(s, user)

    with TestClient(fastapi_app) as c:
        yield c


@pytest.fixture()
def admin_token(client):
    # Avoid calling the /auth/token endpoint in tests (it can be flaky
    # if the app's lifespan or file-backed DB differs). Instead, create
    # a signed JWT directly for the admin user.
    from app.auth import create_access_token

    return create_access_token(data={"sub": "admin"})
