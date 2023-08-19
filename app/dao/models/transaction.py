# app/dao/models/transaction.py
from sqlalchemy import Integer, Enum, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from .base import BaseORMVersioned
from datetime import datetime

class Transaction(BaseORMVersioned):
    __tablename__ = "transaction"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id", ondelete='CASCADE'))
    portfolio_id: Mapped[int] = mapped_column(Integer, ForeignKey("portfolio.id", ondelete='CASCADE'))
    transaction_type: Mapped[str] = mapped_column(Enum('BUY', 'SELL', 'DIVIDEND', 'STOCK_SPLIT', name='transaction_types'))
    transaction_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # Date the transaction took place
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    fees: Mapped[float] = mapped_column(Float)
    
    # Relationships
    # one-to-many -> (A User's Portfolio) - has - (Transactions associated with a stock)
    portfolio: Mapped["UserPortfolio"] = relationship("UserPortfolio", back_populates="transactions")

    def __repr__(self):
        return (f"ORM: <Transaction(id={self.id}, stock_id={self.stock_id}, "
                f"transaction_type={self.transaction_type}, transaction_date={self.transaction_date}, "
                f"quantity={self.quantity}, price={self.price}, fees={self.fees})>")

    @validates('price')
    def validate_price(self, key, price):
        if self.transaction_type in ('DIVIDEND', 'STOCK_SPLIT'):
            return 0  # Set price to zero for DIVIDEND and STOCK_SPLIT transactions
        return price
