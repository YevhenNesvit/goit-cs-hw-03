import psycopg2
import os
import dotenv

from contextlib import contextmanager


# Завантаження файлу .env
dotenv.load_dotenv()

@contextmanager
def create_connect():
    try:
        conn = psycopg2.connect(host="localhost", database="postgres", user=os.getenv("DB_USERNAME"), password=os.getenv("DB_PASSWORD"))
        try:
            yield conn
        finally:
            conn.close()
    except psycopg2.OperationalError:
        print("Connection failed")