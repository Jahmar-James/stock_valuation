# app/dao/models/user_portfolio.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class UserPortfolio(BaseModel):

    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    name = Column(String)
    description = Column(String)
    creation_date = Column(DateTime, default=datetime.utcnow)
    type = Column(String) # "paper" or "real" Taxable or Tax-Deferred, etc.
    user = relationship("User", back_populates="portfolios")  # Each portfolio is related to one user
    transactions = relationship("Transaction", back_populates="portfolio") # real | Each portfolio has one set of transactions
    holdings = relationship("Holding", back_populates="portfolio") # paper | Each portfolio has one set of holdings