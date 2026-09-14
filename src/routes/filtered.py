from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.templating import _TemplateResponse

from ..api.the_meal_db import get_meals_categories

router: APIRouter = APIRouter()


router.mount(path="/static", app=StaticFiles(directory="static"), name="static")

templates: Jinja2Templates = Jinja2Templates(directory="static/templates")

@router.get(path="/user/{id}/{filter}")
async def read_filtered(request: Request, id:int, filter: str) -> _TemplateResponse:
    return templates.TemplateResponse(
        request=request,
        name="filtered.html",
        status_code=200,
        context={
            "id": id,
            "filter" : filter
        },
    )