# app/dao/models/document.py

from sqlalchemy import Integer, String, ForeignKey, CheckConstraint, Text, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from .base import BaseORMVersioned

class Document(BaseORMVersioned):
    __tablename__ = "document"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String, index=True, unique=True)
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[bytes] = mapped_column(LargeBinary)
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id", ondelete='SET NULL'), nullable=True)
    sector_id: Mapped[int] = mapped_column(Integer, ForeignKey("sector.id", ondelete='SET NULL'), nullable=True)

    # Constraints
    __table_args__ = (
        CheckConstraint('stock_id IS NOT NULL OR sector_id IS NOT NULL', name='chk_stock_sector_presence'),
    )
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename}, content_length={len(self.content)})>"
