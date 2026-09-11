from pydantic import BaseModel
from pydantic.networks import EmailStr

from .activity import ActivityLevelEnum
from .goal import GoalEnum
from .sexe import SexeEnum


class User_Stats(BaseModel):
    FirstName: str
    LastName: str
    Username: str
    Email: EmailStr
    Password: str  # TODO : A HASH
    Sexe: SexeEnum
    Poids: float  # En kg
    Taille: int  # en cm
    Age: int
    ActivityLevel: ActivityLevelEnum
    Goal: GoalEnum
