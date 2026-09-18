from fastapi import FastAPI

from .src.routes import debug, details, filtered, health, root, user, user_stat

app: FastAPI = FastAPI()

app.include_router(root.router)
app.include_router(health.router)
app.include_router(user.router)
app.include_router(user_stat.router)
app.include_router(filtered.router)
app.include_router(debug.router)
app.include_router(details.router)
