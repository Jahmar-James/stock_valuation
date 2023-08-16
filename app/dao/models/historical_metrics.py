# app/dao/models/historical_metrics.py
from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class HistoricalMetrics(BaseModel):
    """
    Quarterly key historical metrics for a stock
    """
    __tablename__ = "historical_metric"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"))
    date = Column(Date)
    revenue = Column(Float)
    net_income = Column(Float)
    price_to_earnings = Column(Float)
    price_to_book = Column(Float)
    price_to_sales = Column(Float)
    price_to_cashflow = Column(Float)
    price_to_earnings_growth = Column(Float)
    dividend_yield = Column(Float)
    payout_ratio = Column(Float)
    shares_outstanding = Column(Float)
    market_cap = Column(Float)
    enterprise_value = Column(Float)
    enterprise_value_to_revenue = Column(Float)
    return_on_equity = Column(Float)
    return_on_investment = Column(Float)
    
    stock = relationship("Stock", back_populates="historical_metrics")
