import os
from typing import Any, Dict, List

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter
from starlette import responses
from starlette.exceptions import HTTPException

from ..utils.formatter import api_formatter

router: APIRouter = APIRouter()

load_dotenv()

USDA_API_KEY = os.getenv("USDA_API_KEY")


async def get_food(food: str, limit: int = 5) -> List[Dict[str, Any]]:
    res: List[Dict[str, Any]] = []
    url: str = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={USDA_API_KEY}&query={food}&pageSize={limit}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            foods_list = data.get("foods", [])
            if not isinstance(foods_list, list):
                raise HTTPException(
                    status_code=500,
                    detail="Invalid API response format: 'foods' is not a list",
                )

            for food_item in foods_list:
                food_info = {
                    "id": food_item.get("fdcId"),
                    "name": food_item.get("description"),
                    "category": food_item.get("foodCategory"),
                    "published_at": food_item.get("publishedDate"),
                    "nutrients": {
                        nutrient.get("nutrientName"): {
                            "value": nutrient.get("value"),
                            "unit": nutrient.get("unitName"),
                        }
                        for nutrient in food_item.get("foodNutrients", [])
                    },
                }
                res.append(food_info)

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail="API request failed"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return res
