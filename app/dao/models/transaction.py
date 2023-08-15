# app/dao/models/"transaction.py
from sqlalchemy import Column, Integer, Enum,  Float, Date, ForeignKey
from .base import BaseModel
from sqlalchemy.orm import validates


class Transaction(BaseModel):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete='CASCADE'))
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete='CASCADE'))
    transaction_type = Column(Enum('BUY', 'SELL', 'DIVIDEND','STOCK_SPLIT', name='transaction_types'))
    transaction_date = Column(Date)
    quantity = Column(Integer)
    price = Column(Float)
    fees = Column(Float)
    

    @validates('price')
    def validate_price(self, key, price):
        if self.transaction_type in ('DIVIDEND', 'STOCK_SPLIT'):
            return 0  # Set price to zero for DIVIDEND and STOCK_SPLIT transactions
        return price