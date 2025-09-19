import os
import sys
from pathlib import Path
import json
import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

# ensure project root on path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from main import app
from app.db import get_session
from app.models import User
from app.auth import get_password_hash


@pytest.fixture(scope="session")
def engine():
    # in-memory sqlite for tests
    url = "sqlite:///:memory:"
    engine = create_engine(url, connect_args={"check_same_thread": False})
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

    monkeypatch.setattr("app.db.get_session", get_session_override)

    # ensure ADMIN_PASSWORD is set so lifespan init creates admin user
    os.environ.setdefault("ADMIN_PASSWORD", "testadmin")

    with TestClient(app) as c:
        yield c


@pytest.fixture()
def admin_token(client):
    admin_pw = os.environ.get("ADMIN_PASSWORD", "testadmin")
    r = client.post("/auth/token", data={"username": "admin", "password": admin_pw})
    assert r.status_code == 200
    return r.json()["access_token"]
