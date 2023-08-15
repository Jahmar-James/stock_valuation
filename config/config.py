# config\config.py
import os

DATABASE_URL = "postgresql://username:password@localhost:5432/mydatabase"

class Config:
    DB_TEST = os.getenv("DB_TEST", 'sqlite:///data/db.sqlite3')
    DB_HOST = os.getenv("DB_HOST", DATABASE_URL)