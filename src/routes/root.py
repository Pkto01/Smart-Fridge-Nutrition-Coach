from fastapi import APIRouter


router: APIRouter = APIRouter()

# TODO : redirection de la route vers le user sauvergardé dans le cache du navigateur + check BDD

@router.get("/")
async def read_users() -> dict[str, str]:
    return {"message": "salut"}