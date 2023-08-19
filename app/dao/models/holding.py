# app/dao/models/holding.py

from sqlalchemy import Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import BaseORMVersioned
from datetime import datetime

class Holding(BaseORMVersioned):
    __tablename__ = "holding"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    portfolio_id: Mapped[int] = mapped_column(Integer, ForeignKey("portfolio.id", ondelete='CASCADE'))
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id", ondelete="RESTRICT"), index=True)
    quantity: Mapped[float] = mapped_column(Float)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    average_cost_basis: Mapped[float] = mapped_column(Float)

    # Relationships
    # one-to-many -> (A User's paper Portfolio) - has - (Holdings associated with a stock)
    portfolio: Mapped["UserPortfolio"] = relationship("UserPortfolio", back_populates="holdings")
    # one-to-many -> (A Stock) - is represented in - (Holdings)
    stock: Mapped["Stock"] = relationship("Stock", back_populates="holding")

    def __repr__(self):
        return (f"ORM: <Holding(id={self.id}, stock_id={self.stock_id}, quantity={self.quantity}, "
                f"date={self.date}, average_cost_basis={self.average_cost_basis})>")
