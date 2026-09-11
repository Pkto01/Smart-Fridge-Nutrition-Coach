from fastapi import APIRouter


router: APIRouter = APIRouter()

@router.get("/")
async def read_users() -> dict[str, str]:
    return {"message": "salut"}