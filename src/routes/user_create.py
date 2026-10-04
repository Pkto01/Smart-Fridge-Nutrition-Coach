from pydantic import BaseModel
from fastapi import status, HTTPException
from fastapi import APIRouter

from ..databaseConn import createUser

router: APIRouter = APIRouter()

class UserCreate(BaseModel):
    FirstName: str
    LastName: str
    Username: str
    Email: str
    password: str
    gender: str
    weight: float
    height: int
    age: int
    ActivityLevel: str
    goal: str


@router.post(path="/create_user/creating", status_code=status.HTTP_201_CREATED)
async def user_create(user_data: UserCreate):
    try:

        createUser.create_user(user_data)
        
        return {"message": "Utilisateur créé avec succès", "data": user_data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'enregistrement en BDD: {str(e)}"
        )