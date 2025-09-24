import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import init_db, init_admin_user
from .routers import auth, devices, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    init_db()
    init_admin_user(os.environ.get("ADMIN_PASSWORD"))
    yield
    # shutdown (nothing for now)


app = FastAPI(title="IoT Sensors Enrichment", lifespan=lifespan)


def _get_app_version():
    """Return the application version.

    Priority:
    1. VERSION environment variable (set by CI/build)
    2. VERSION file at project root (optional)
    3. fallback to 'dev'
    """
    v = os.environ.get("VERSION")
    if v:
        return v
    try:
        with open("VERSION", "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return "dev"


APP_VERSION = _get_app_version()


@app.get("/")
async def read_root():
    return {"message": f"Hello, from {app.title}!", "version": APP_VERSION}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(devices.router)
# app package
