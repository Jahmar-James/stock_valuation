# app/dao/models/user_portfolio.py
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import BaseORMVersioned

class UserPortfolio(BaseORMVersioned):

    __tablename__ = 'portfolio'

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    creation_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    type: Mapped[str] = mapped_column(String) # "paper" or "real" Taxable or Tax-Deferred, etc.

    # Relationships
    # one-to-many -> (user)-has-(portfolios)
    user = relationship("User", back_populates="portfolios")
    # one-to-many -> (real portfolio)-has-(transactions)
    transactions: Mapped["Transaction"] = relationship("Transaction", back_populates="portfolio")
    # one-to-many -> (paper portfolio)-has-(holdings)
    holdings: Mapped["Holding"] = relationship("Holding", back_populates="portfolio")

    def __repr__(self):
        return f"ORM: <Portfolio(id={self.id}, name={self.name}, description={self.description}, creation_date={self.creation_date}, type={self.type})>"