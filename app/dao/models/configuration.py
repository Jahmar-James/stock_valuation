# app/dao/models/configuration.py
from sqlalchemy import Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import BaseORMVersioned

class Configuration(BaseORMVersioned):
    """User-specific configuration settings - one per user"""
    __tablename__ = "configuration"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete='CASCADE'), unique=True)
    settings: Mapped[dict] = mapped_column(JSON, nullable=False)

    # Relationships
    # one-to-one -> (A User) - has - (One Configuration)
    user: Mapped["User"] = relationship("User", back_populates="configuration")

    def __repr__(self):
        return f"<Configuration(id={self.id}, user_id={self.user_id}, settings={self.settings})>"

if __name__ == "__main__":
    # your testing code here
    print("Testing Configuration ORM")
