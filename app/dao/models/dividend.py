# app/dao/models/dividend.py
from sqlalchemy import Column, Integer, ForeignKey,  Float, Date
from sqlalchemy.orm import relationship
from .base import BaseModel

class Dividend(BaseModel):
    __tablename__ = "dividend"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id",ondelete='CASCADE'))
    date = Column(Date)
    dividend = Column(Float)

    stock = relationship("Stock", back_populates="dividend")