# app/dao/models/dividend.py

from sqlalchemy import Integer, ForeignKey, Float, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import BaseORMVersioned

class Dividend(BaseORMVersioned):
    __tablename__ = "dividend"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id", ondelete='CASCADE'))
    date: Mapped[Date] = mapped_column(Date)
    dividend: Mapped[float] = mapped_column(Float)

    # Relationships
    # one-to-many -> (A Stock) - has - (Dividends over time)
    stock: Mapped["Stock"] = relationship("Stock", back_populates="dividends")

    def __repr__(self):
        return f"ORM: <Dividend(id={self.id}, stock_id={self.stock_id}, date={self.date}, dividend={self.dividend})>"
