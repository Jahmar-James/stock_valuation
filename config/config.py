# config\config.py
import os

class Config:
    DB_HOST = os.getenv("DB_HOST", "sql::://data/db.sqlite3")