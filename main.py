from contextlib import asynccontextmanager

from fastapi import FastAPI

from .src.databaseConn.database import init_db, pool
from .src.databaseConn import userConnection
from .src.routes import (
    connection,
    debug,
    details,
    filtered,
    health,
    meals,
    profile,
    root,
    user,
    user_create,
    user_stat,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    pool.close()


app = FastAPI(lifespan=lifespan)

app.include_router(root.router)
app.include_router(health.router)
app.include_router(user.router)

app.include_router(user_stat.router)
app.include_router(filtered.router)
app.include_router(debug.router)
app.include_router(details.router)
app.include_router(meals.router)

app.include_router(user_create.router)
app.include_router(connection.router)
app.include_router(userConnection.router)
app.include_router(profile.router)