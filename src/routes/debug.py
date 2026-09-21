from fastapi import APIRouter

from ..api.usda import get_food

router: APIRouter = APIRouter()

@router.get("/debug/{food}")
async def search_food(food: str):
    return await get_food(food)

