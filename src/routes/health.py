from fastapi import APIRouter

router: APIRouter = APIRouter()


@router.get(path="/health")
async def read_users() -> dict[str, str]:
    return {"status": "ok"}
