# app/dao/models/historical_price.py

from sqlalchemy import Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import BaseORMVersioned

class HistoricalPrice(BaseORMVersioned):
    """Daily historical prices for a stock"""
    __tablename__ = "historical_price"

    # Columns
    date: Mapped[Date] = mapped_column(Date, primary_key=True)
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id", ondelete='CASCADE'), primary_key=True)
    open_price: Mapped[float] = mapped_column(Float)
    close_price: Mapped[float] = mapped_column(Float, index=True)
    high_price: Mapped[float] = mapped_column(Float)
    low_price: Mapped[float] = mapped_column(Float)

    # Relationships
    # one-to-many -> (A Stock) - has - (Historical Prices over time)
    stock: Mapped["Stock"] = relationship("Stock", back_populates="historical_prices")

    def __repr__(self):
        return (f"<HistoricalPrice(date={self.date}, stock_id={self.stock_id}, open_price={self.open_price}, "
                f"close_price={self.close_price}, high_price={self.high_price}, low_price={self.low_price})>")
