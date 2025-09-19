from fastapi import FastAPI
import uvicorn
from app.routers import devices, users, auth
from app.db import init_db, init_admin_user
from contextlib import asynccontextmanager
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    init_db()
    init_admin_user(os.environ.get("ADMIN_PASSWORD"))
    yield
    # shutdown (nothing for now)


app = FastAPI(title="IoT Sensors Enrichment", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(devices.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
