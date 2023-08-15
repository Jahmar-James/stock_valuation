# app/dao/models/stock_sector.py
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import BaseModel

stock_sector_association = Table('stock_sector', BaseModel.metadata,
    Column('stock_id', Integer, ForeignKey('stock.id')),
    Column('sector_id', Integer, ForeignKey('sector.id'))
)

class Stock(BaseModel):
    """
    Represents a stock in the database. 
    - DAO (Data Access Object) 

    Attributes:
        id (int): The auto-incrementing primary key for the stock.
        ticker_symbol (str): The ticker symbol of the stock (e.g., AAPL).
        historical_prices (Relationship): One-to-many relationship with HistoricalPrice.
        dividends (Relationship): One-to-many relationship with Dividend.
    """
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    ticker_symbol = Column(String, index=True, unique=True)
    company_name = Column(String)
    
    historical_prices = relationship("HistoricalPrice", back_populates="stock", )
    dividends = relationship("Dividend", back_populates="stock")
    sectors = relationship("Sector", secondary=stock_sector_association, back_populates="stock")
    historical_metrics = relationship("HistoricalMetric", back_populates="stock")

class Sector(BaseModel):
    __tablename__ = "sector"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    
    stocks = relationship("Stock", secondary=stock_sector_association, back_populates="sector")