import datetime
import hashlib
import hmac
import jwt
import os
from dotenv import load_dotenv

from psycopg.rows import dict_row
from .database import get_db, pool

load_dotenv()

SECRET_KEY = os.getenv("DB_URL")
ALGORITHM = "HS256"


def login_user(login_data) -> dict:
    raw_password = login_data.password
    input_password_hash = hashlib.sha512(raw_password.encode("utf-8")).hexdigest()

    query = """
        select 
            id,
            first_name, 
            last_name, 
            email, 
            username, 
            password_hash, 
            gender, 
            weight, 
            height, 
            age, 
            ActivityLevel, 
            goal
        from users
        where email = %(email)s;
    """

    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, {"email": login_data.mail})
            user = cur.fetchone()

    if not user:
        return {"error": "Identifiants invalides"}

    stored_hash = user["password_hash"]
    if not hmac.compare_digest(input_password_hash, stored_hash):
        return {"error": "Identifiants invalides"}

    # Génération du payload du JWT
    expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)  # Expiration dans 1 jour
    payload = {
        "sub": str(user["id"]),
        "email": user["email"],
        "username": user["username"],
        "exp": expiration,  # Expiration du token
        "iat": datetime.datetime.now(datetime.timezone.utc),  # Issued at
    }

    # Signature du token avec PyJWT
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # Nettoyage des données sensibles avant retour
    del user["password_hash"]

    return {
        "message": "Connexion réussie",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }