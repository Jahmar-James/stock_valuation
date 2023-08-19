# app/dao/models/user.py
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import BaseORMVersioned

class User(BaseORMVersioned):
    """User of the application, for multiple local users"""
    __tablename__ = "users"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    last_login: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    permission: Mapped[str] = mapped_column(Enum('ADMIN', 'USER', name='permissions'), default='USER')
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    
    # Relationships
    portfolios: Mapped["UserPortfolio"] = relationship("UserPortfolio", back_populates="user", cascade="all, delete-orphan")
    configuration: Mapped["Configuration"] = relationship("Configuration", uselist=False, back_populates="user")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"
