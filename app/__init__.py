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


@app.get("/")
async def read_root():
    return {"message": f"Hello, from {app.title}!"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(devices.router)
# app package
