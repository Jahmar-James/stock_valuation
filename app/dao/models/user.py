# app/dao/models/user.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel

class User(BaseModel):
    """User of the application, for multiple local users"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    last_login = Column(DateTime, default=datetime.utcnow)
    permission = Column(Enum('ADMIN', 'USER', name='permissions'), default='USER')
    hashed_password = Column(String, nullable=False)
    portfolios = relationship("UserPortfolio", back_populates="user", cascade="all, delete-orphan")
    configuration = relationship("Configuration", uselist=False, back_populates="user")