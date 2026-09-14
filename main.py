from contextlib import asynccontextmanager

from fastapi import FastAPI


from .src.routes import health, root, user, user_stat, debug, filtered


from .src.routes import health, root, user, user_stat, debug, filtered
from .src.databaseConn.database import init_db, pool


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

