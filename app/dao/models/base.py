# app/dao/models/base.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config

engine = create_engine(Config.DB_HOST)
SessionLocal = sessionmaker(bind=engine)
