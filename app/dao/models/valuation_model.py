# app/dao/models/valuation_model.py
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Float, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from .base import BaseORMVersioned

class ValuationModel(BaseORMVersioned):

    __tablename__ = "valuation_model"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id", ondelete='SET NULL'))
    valuation_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    valuation_method: Mapped[str] = mapped_column(String, nullable=False)  # Name/Type of the strategy used
    valuation_result: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    assumptions: Mapped[str] = mapped_column(JSON, nullable=True)  # JSON string containing the assumptions used for the valuation
    parameters: Mapped[str] = mapped_column(JSON, nullable=True)  # JSON string containing the parameters used for the valuation
    file_path: Mapped[str] = mapped_column(String, index=True, unique=True)  # Path to the file containing the valuation report | CSV or Excel file
    #<stock_symbol>_<valuation_method>_<valuation_date>.csv

    def __repr__(self):
        return (f"<ValuationModel(id={self.id}, stock_id={self.stock_id}, "
                f"valuation_date={self.valuation_date}, valuation_method={self.valuation_method}, "
                f"valuation_result={self.valuation_result})>")

