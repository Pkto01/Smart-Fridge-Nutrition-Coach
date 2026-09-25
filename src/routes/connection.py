from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.templating import _TemplateResponse

from ...src.api import the_meal_db

router: APIRouter = APIRouter()


router.mount(path="/static", app=StaticFiles(directory="static"), name="static")

templates: Jinja2Templates = Jinja2Templates(directory="static/templates")


@router.get(path="/connection", response_class=HTMLResponse)
async def read_users(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(
        request=request,
        name="connection.html",
        status_code=200,
    )
