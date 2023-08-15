# app/dao/models/configuration.py
from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class Configuration(BaseModel):
    """User-specific configuration settings - one per user"""
    __tablename__ = "configuration"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), unique=True)
    settings= Column(JSON, nullable=False)
    
    user = relationship("User", back_populates="configuration")
    
if __name__ == "__main__":
    # your testing code here
    print("Testing Configuration ORM")
