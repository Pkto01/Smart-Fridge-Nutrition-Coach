import difflib
import re
from typing import Any, Dict, List, Optional

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from ..api.bridge import find_meals_for_food

router: APIRouter = APIRouter()


router.mount(path="/static", app=StaticFiles(directory="static"), name="static")

templates: Jinja2Templates = Jinja2Templates(directory="static/templates")


@router.get("/bridge")
async def bridge_food_to_meals(food: str, limit: int = 5) -> List[Dict[str, Any]]:
    from ..api.usda import get_food

    foods = await get_food(food, limit=limit)
    results = []
    for f in foods:
        results.append(await find_meals_for_food(f))
    return results


@router.get("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = "", limit: int = 5):
    results = []
    if query:
        results = await bridge_food_to_meals(query, limit)
    return templates.TemplateResponse(
        request=request,
        name="search.html",
        context={
            "request": request,
            "query": query,
            "limit": limit,
            "results": results,
        },
    )
