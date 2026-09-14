from fastapi import APIRouter

from ..models import user_stats

router: APIRouter = APIRouter()


@router.post(path="/api/user_stats/")
async def post_user_stat(user_stats: user_stats.User_Stats) -> user_stats.User_Stats:
    return user_stats