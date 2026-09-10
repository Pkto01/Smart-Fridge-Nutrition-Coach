from fastapi import FastAPI

from .src.routes import health, root

app: FastAPI = FastAPI()

app.include_router(root.router)
app.include_router(health.router)
