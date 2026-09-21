import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

load_dotenv()

DB_URL = os.getenv("DB_URL")


pool = ConnectionPool(conninfo=DB_URL, open=False)


def init_db():
    pool.open()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    gender VARCHAR(10),
                    weight FLOAT,
                    height FLOAT,
                    age INT,
                    ActivityLevel VARCHAR(50),
                    goal VARCHAR(30)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fridge_items (
                    id SERIAL PRIMARY KEY,
                    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    ingredient_name VARCHAR(255) NOT NULL,
                    quantity FLOAT,
                    unit VARCHAR(50)
                );
            """)
            conn.commit()


def get_db():
    with pool.connection() as conn:
        conn.row_factory = dict_row
        yield conn
