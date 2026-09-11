from pydantic import BaseModel

from .activity import ActivityLevelEnum
from .goal import GoalEnum


class User_Stats(BaseModel):
    FirstName: str
    LastName: str
    Username: str
    Email: str
    Password: str  # TODO : A HASH
    Poids: float  # En kg
    Taille: int  # en cm
    Age: int
    ActivityLevel: ActivityLevelEnum
    Goal: GoalEnum
