import difflib
import re
from typing import Any, Dict, List, Optional

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates

router: APIRouter = APIRouter()

# Cache simple en mémoire pour éviter de re-fetch la liste à chaque requête
_ingredient_cache: Optional[List[str]] = None


async def get_mealdb_ingredients(client: httpx.AsyncClient) -> List[str]:
    global _ingredient_cache
    if _ingredient_cache is not None:
        return _ingredient_cache

    url = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
    response = await client.get(url)
    response.raise_for_status()
    data = response.json()

    ingredients = [
        item.get("strIngredient", "").strip()
        for item in data.get("meals", []) or []
        if item.get("strIngredient")
    ]
    _ingredient_cache = ingredients
    return ingredients


def clean_usda_name(usda_description: str) -> List[str]:
    """
    Génère plusieurs candidats simples à partir d'une description USDA,
    du plus spécifique au plus générique.
    Ex: 'Chicken, breast, boneless, skinless, raw' ->
        ['chicken breast boneless', 'chicken breast', 'chicken']
    """
    parts = [p.strip().lower() for p in usda_description.split(",") if p.strip()]
    parts = [re.sub(r"[^a-z\s]", "", p).strip() for p in parts]
    parts = [p for p in parts if p]

    candidates = []
    if parts:
        # le nom principal (premier segment) est le candidat de base
        candidates.append(parts[0])
        # on ajoute des combinaisons décroissantes en partant du + spécifique
        for i in range(len(parts), 0, -1):
            candidates.append(" ".join(parts[:i]))
    # dédoublonnage en gardant l'ordre
    seen = set()
    ordered = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            ordered.append(c)
    return ordered


def best_ingredient_match(
    candidates: List[str], known_ingredients: List[str]
) -> Optional[str]:
    """
    Cherche le meilleur match entre nos candidats et la liste réelle
    d'ingrédients TheMealDB, avec tolérance (singulier/pluriel, fautes).
    """
    known_lower = {ing.lower(): ing for ing in known_ingredients}

    for candidate in candidates:
        # 1. Match exact
        if candidate in known_lower:
            return known_lower[candidate]

        # 2. Match singulier/pluriel simple
        if candidate.endswith("s") and candidate[:-1] in known_lower:
            return known_lower[candidate[:-1]]
        if (candidate + "s") in known_lower:
            return known_lower[candidate + "s"]

        # 3. Match flou (fautes de frappe, variantes proches)
        close = difflib.get_close_matches(
            candidate, known_lower.keys(), n=1, cutoff=0.8
        )
        if close:
            return known_lower[close[0]]

    return None


async def find_meals_for_food(food_item: Dict[str, Any]) -> Dict[str, Any]:
    name = food_item.get("name") or ""
    if not name:
        return {"food": food_item, "matched_ingredient": None, "meals": []}

    candidates = clean_usda_name(name)

    async with httpx.AsyncClient() as client:
        known_ingredients = await get_mealdb_ingredients(client)
        matched = best_ingredient_match(candidates, known_ingredients)

        meals: List[Dict[str, Any]] = []
        if matched:
            # TheMealDB veut des underscores pour les ingrédients multi-mots
            query_value = matched.replace(" ", "_")
            url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={query_value}"
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                meals = data.get("meals") or []
            except httpx.HTTPStatusError:
                meals = []

    simplified_meals = [
        {
            "id": m.get("idMeal"),
            "name": m.get("strMeal"),
            "thumbnail": m.get("strMealThumb"),
        }
        for m in meals
    ]

    return {
        "food": food_item,
        "matched_ingredient": matched,
        "candidates_tried": candidates,
        "meals": simplified_meals,
    }


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
        results = await   bridge_food_to_meals(query, limit)# ta logique existante
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
