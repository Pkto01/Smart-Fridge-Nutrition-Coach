from fastapi import HTTPException
from psycopg import Connection

def get_user_by_id(user_id: int, conn: Connection) -> dict:
    """
    Cherche un utilisateur en BDD par son ID.
    Retourne un dictionnaire avec les données ou lève une HTTPException 404 si introuvable.
    """
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, email, age, gender, weight, height, activity_level, goal, created_at 
            FROM users 
            WHERE id = %s;
            """,
            (user_id,)
        )
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(
                status_code=404, 
                detail=f"Utilisateur avec l'ID {user_id} non trouvé"
            )
            
        return user