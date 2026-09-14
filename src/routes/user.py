from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.templating import _TemplateResponse

from ..models import activity, goal, sexe

router: APIRouter = APIRouter()


router.mount(path="/static", app= StaticFiles(directory="static"), name="static")

templates: Jinja2Templates = Jinja2Templates(directory="static/templates")


ACTIVITY = activity.ActivityLevelEnum
GOAL = goal.GoalEnum
SEXE = sexe.SexeEnum

@router.get(path="/user/{id}", response_class=HTMLResponse)
async def read_users(request: Request, id: int) -> _TemplateResponse:
    return templates.TemplateResponse(request=request, name="index.html", status_code=200, context={
        "id": id,
        "activity": ACTIVITY,
        "goal": GOAL,
        "sexe": SEXE
    })
