from importlib import import_module

import uvicorn

# import the package app which exposes the FastAPI instance
app = import_module("app").app


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
