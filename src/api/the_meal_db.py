import httpx
from fastapi import APIRouter

router = APIRouter()


async def get_meals_categories() -> list[str]:
    res: list[str] = []
    url = "https://www.themealdb.com/api/json/v1/1/list.php?c=list"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            for category in data.get("meals", []):
                res.append(category.get("strCategory", ""))
    return res
