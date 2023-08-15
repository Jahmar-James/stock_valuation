# app/dao/models/holding.py

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Holding(BaseModel):
    __tablename__ = "holding"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete='CASCADE'))
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="RESTRICT"),index=True)
    quantity = Column(Integer)
    average_cost_basis = Column(Float)
    
    portfolio = relationship("UserPortfolio", back_populates="holding")
    stock = relationship("Stock", back_populates="holding")