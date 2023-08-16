# app/dao/models/holding.py

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel
from datetime import datetime

class Holding(BaseModel):
    __tablename__ = "holding"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolio.id", ondelete='CASCADE'))
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="RESTRICT"),index=True)
    quantity = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    average_cost_basis = Column(Float)
    
    portfolio = relationship("UserPortfolio", back_populates="holdings")
    stock = relationship("Stock", back_populates="holding")