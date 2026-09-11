from fastapi import APIRouter

from ..models import user_stats

router: APIRouter = APIRouter()


@router.post(path="/api/user_stats/", status_code=201)
async def postuser_stat(user_stats: user_stats.User_Stats):
    return { "message" : user_stats}
