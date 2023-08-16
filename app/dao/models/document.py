# app/dao/models/document.py
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Text, LargeBinary
from .base import BaseModel

class Document(BaseModel):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True, unique=True)
    content = Column(Text)
    embedding = Column(LargeBinary) 
    
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete='SET NULL'), nullable=True)
    sector_id = Column(Integer, ForeignKey("sector.id", ondelete='SET NULL'), nullable=True)

    __table_args__ = (
        CheckConstraint('stock_id IS NOT NULL OR sector_id IS NOT NULL',
                        name='chk_stock_sector_presence'),
    )