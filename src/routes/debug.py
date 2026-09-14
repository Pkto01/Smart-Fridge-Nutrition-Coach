from fastapi import APIRouter

router: APIRouter = APIRouter()


@router.get(path="/debug")
async def read_debug():
    return {"message": "DEBUG"}
