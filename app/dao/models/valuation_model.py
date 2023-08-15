# app/dao/models/valuation_model.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text

from .base import BaseModel

class ValuationModel(BaseModel):
    """
    Represents a stock valuation in the database.
    DAO (Data Access Object): An object that provides an abstract interface to some database or other persistence mechanism.
    """
    __tablename__ = "valuation_model"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete='SET NULL'))
    valuation_date = Column(DateTime, default=datetime.utcnow)
    valuation_method = Column(String, nullable=False)  # Name/Type of the strategy used
    valuation_result = Column(Float, nullable=False, index=True)
    assumptions = Column(Text, nullable=True)  # JSON string containing the assumptions used for the valuation
    parameters = Column(Text, nullable=True)  # JSON string containing the parameters used for the valuation
    file_path = Column(String, index=True, unique=True)  # Path to the file containing the valuation report | CSV or Excel file
    #<stock_symbol>_<valuation_method>_<valuation_date>.csv