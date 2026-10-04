import hashlib
from psycopg.rows import dict_row
from .database import get_db, pool


def create_user(user_data: dict) -> dict:
    raw_password = user_data.password
    password_hash = hashlib.sha512(raw_password.encode("utf-8")).hexdigest()

    query = """
        INSERT INTO users (
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
        )
        VALUES (
            %(first_name)s, 
            %(last_name)s, 
            %(email)s, 
            %(username)s, 
            %(password_hash)s, 
            %(gender)s, 
            %(weight)s, 
            %(height)s, 
            %(age)s, 
            %(ActivityLevel)s, 
            %(goal)s
        )
        RETURNING id, username, email;
    """

    payload = {
        "first_name": user_data.FirstName,
        "last_name": user_data.LastName,
        "email": user_data.Email,
        "username": user_data.Username,
        "password_hash": password_hash,
        "gender": user_data.gender,
        "weight": user_data.weight,
        "height": user_data.height,
        "age": user_data.age,
        "ActivityLevel": user_data.ActivityLevel,
        "goal": user_data.goal,
    }

    with pool.connection() as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cursor:
            cursor.execute(query, payload)
            new_user = cursor.fetchone()
            conn.commit()
            return new_user