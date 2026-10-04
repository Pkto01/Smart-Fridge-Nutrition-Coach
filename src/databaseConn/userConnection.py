from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status
from fastapi.staticfiles import StaticFiles
import hashlib
import jwt
import os
from psycopg.rows import dict_row
from fastapi import Response

from .database import get_db, pool

load_dotenv()

SECRET_JWT_KEY = os.getenv("SECRET_JWT_KEY")
ALGORITHM = "HS256"

router: APIRouter = APIRouter()

router.mount(path="/static", app=StaticFiles(directory="static"), name="static")

@router.post("/token") 
def login(form_data: dict, response: Response):
    query = """
        SELECT * FROM users
        WHERE email = %(email)s;
    """

    payload = {
        "email": form_data.get("email")
    }

    with pool.connection() as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cursor:
            cursor.execute(query, payload)
            user = cursor.fetchone()

    raw_password = form_data.get("password", "")
    input_password_hash = hashlib.sha512(raw_password.encode("utf-8")).hexdigest()

    if not user or user["password_hash"] != input_password_hash:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect email or password"
        )

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    token_payload = {
        "sub": user["email"], 
        "exp": expire
    }
    token = jwt.encode(token_payload, SECRET_JWT_KEY, algorithm=ALGORITHM)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=1800
    )

    return {"message": "Connexion réussie"}