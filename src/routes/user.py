from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.templating import _TemplateResponse

from ...src.api import the_meal_db
from ..models import activity, goal, sexe

router: APIRouter = APIRouter()


router.mount(path="/static", app=StaticFiles(directory="static"), name="static")

templates: Jinja2Templates = Jinja2Templates(directory="static/templates")


ACTIVITY = activity.ActivityLevelEnum
GOAL = goal.GoalEnum
SEXE = sexe.SexeEnum


@router.get(path="/create_user", response_class=HTMLResponse)
async def read_users(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(
        request=request,
        name="create_profile.html",
        status_code=200,
        context={
            "activity": ACTIVITY,
            "goal": GOAL,
            "sexe": SEXE,
            # Front relative
            "meals": await the_meal_db.get_meals_categories(),
        },
    )
