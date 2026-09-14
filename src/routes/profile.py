from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from psycopg import Connection
from starlette.templating import _TemplateResponse

# Importe ta fonction et la dépendance BDD
from ...src.databaseConn.database import get_db
from ...src.databaseConn.getUser import get_user_by_id

router: APIRouter = APIRouter()

templates: Jinja2Templates = Jinja2Templates(directory="static/profile")

@router.get(path="/profile/{id}", response_class=HTMLResponse)
async def read_users(request: Request, id: int, conn: Connection = Depends(get_db)) -> _TemplateResponse:
    user = get_user_by_id(user_id=id, conn=conn)
    
    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={"user": user}
    )