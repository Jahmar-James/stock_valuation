# config\config.py
import os

DATABASE_URL = "postgresql://username:password@localhost:5432/mydatabase"

class Config:
    DB_HOST = os.getenv("DB_HOST", "sql::://data/db.sqlite3")