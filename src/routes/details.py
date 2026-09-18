import httpx
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette import responses
from starlette.requests import Request
from starlette.templating import _TemplateResponse

from ..api.the_meal_db import get_meals_categories

router: APIRouter = APIRouter()


router.mount(path="/static", app=StaticFiles(directory="static"), name="static")

templates: Jinja2Templates = Jinja2Templates(directory="static/templates")


async def details_process(id: int) -> list[dict]:
    res: list[dict] = []
    url: str = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            res = data.get("meals", [])
    return res

@router.get("/user/{id}/details/{meal_id}")
async def read_details(request: Request, id: int, meal_id: int) -> _TemplateResponse:
    meals = await details_process(meal_id)
    return templates.TemplateResponse(
        request=request,
        name="details.html",
        status_code=200,
        context={
            "id": id,
            "meals": meals
        },
    )

