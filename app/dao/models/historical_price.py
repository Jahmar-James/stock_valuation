# app/dao/models/historical_price.py
from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class HistoricalPrice(BaseModel):
    """Daily historical prices for a stock"""
    __tablename__ = "historical_price"

    date = Column(Date, primary_key=True)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete='CASCADE'), primary_key=True)
    open_price = Column(Float)
    close_price = Column(Float, index=True)
    high_price = Column(Float)
    low_price = Column(Float)

    stock = relationship("Stock", back_populates="historical_price")