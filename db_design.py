from datetime import datetime

from sqlalchemy import (JSON, Column, Date, DateTime, Enum, Float, ForeignKey,
                        Integer, LargeBinary, String, Table, Text, event)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.schema import CheckConstraint

from app.models.base import Base


class User(Base):
    """User of the application, for multiple local users"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    last_login = Column(DateTime, default=datetime.now)
    permission = Column(Enum('ADMIN', 'USER', name='permissions'), default='USER')
    hashed_password = Column(String, nullable=False)
    portfolios = relationship("Portfolio", back_populates="user", cascade="all, delete-orphan")
    configurations = relationship("Configuration", uselist=False, back_populates="user")


class Configuration(Base):
    """User-specific configuration settings - one per user"""
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), unique=True)
    settings= Column(JSON, nullable=False)
    
    user = relationship("User", back_populates="configurations")

class UserPortfolio(Base):

    __tablename__ = 'portfolios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    name = Column(String)
    description = Column(String)
    creation_date = Column(DateTime, default=datetime.now)
    type = Column(String) # "paper" or "real" Taxable or Tax-Deferred, etc.
    user = relationship("User", back_populates="portfolios")
    transactions = relationship("Transaction", back_populates="portfolio") # real
    holdings = relationship("Holding", back_populates="portfolio") # paper

class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete='CASCADE'))
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="RESTRICT"),index=True)
    quantity = Column(Integer)
    average_cost_basis = Column(Float)
    
    portfolio = relationship("UserPortfolio", back_populates="holdings")
    stock = relationship("Stock", back_populates="holdings")
    

stock_sector_association = Table('stock_sector', Base.metadata,
    Column('stock_id', Integer, ForeignKey('stocks.id')),
    Column('sector_id', Integer, ForeignKey('sectors.id'))
)
class Stock(Base):
    """
    Represents a stock in the database. 
    - DAO (Data Access Object) 

    Attributes:
        id (int): The auto-incrementing primary key for the stock.
        ticker_symbol (str): The ticker symbol of the stock (e.g., AAPL).
        historical_prices (Relationship): One-to-many relationship with HistoricalPrice.
        dividends (Relationship): One-to-many relationship with Dividend.
    """
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    ticker_symbol = Column(String, index=True, unique=True)
    company_name = Column(String)
    
    historical_prices = relationship("HistoricalPrice", back_populates="stock", )
    dividends = relationship("Dividend", back_populates="stock")
    sectors = relationship("Sector", secondary=stock_sector_association, back_populates="stocks")
    historical_metrics = relationship("HistoricalMetric", back_populates="stock")

class HistoricalMetric(Base):
    """
    Quarterly key historical metrics for a stock
    """
    __tablename__ = "historical_metrics"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"))
    date = Column(Date)
    revenue = Column(Float)
    net_income = Column(Float)
    price_to_earnings = Column(Float)
    price_to_book = Column(Float)
    price_to_sales = Column(Float)
    price_to_cashflow = Column(Float)
    price_to_earnings_growth = Column(Float)
    dividend_yield = Column(Float)
    payout_ratio = Column(Float)
    shares_outstanding = Column(Float)
    market_cap = Column(Float)
    enterprise_value = Column(Float)
    enterprise_value_to_revenue = Column(Float)
    return_on_equity = Column(Float)
    return_on_investment = Column(Float)
    
    stock = relationship("Stock", back_populates="historical_metrics")


class Sector(Base):
    __tablename__ = "sectors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    
    stocks = relationship("Stock", secondary=stock_sector_association, back_populates="sectors")

class HistoricalPrice(Base):
    """Daily historical prices for a stock"""
    __tablename__ = "historical_prices"

    date = Column(Date, primary_key=True)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete='CASCADE'), primary_key=True)
    open_price = Column(Float)
    close_price = Column(Float, index=True)
    high_price = Column(Float)
    low_price = Column(Float)

    stock = relationship("Stock", back_populates="historical_prices")

class Dividend(Base):
    __tablename__ = "dividends"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id",ondelete='CASCADE'))
    date = Column(Date)
    dividend = Column(Float)

    stock = relationship("Stock", back_populates="dividends")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True, unique=True)
    content = Column(Text)
    embedding = Column(LargeBinary) 
    
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete='SET NULL'), nullable=True)
    sector_id = Column(Integer, ForeignKey("sectors.id", ondelete='SET NULL'), nullable=True)

    __table_args__ = (
        CheckConstraint('stock_id IS NOT NULL OR sector_id IS NOT NULL',
                        name='chk_stock_sector_presence'),
    )


class ValuationModel(Base):
    """
    Represents a stock valuation in the database.
    DAO (Data Access Object): An object that provides an abstract interface to some database or other persistence mechanism.
    """
    __tablename__ = "valuation_models"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete='SET NULL'))
    valuation_date = Column(DateTime, default=datetime.now)
    valuation_method = Column(String, nullable=False)  # Name/Type of the strategy used
    valuation_result = Column(Float, nullable=False, index=True)
    assumptions = Column(Text, nullable=True)  # JSON string containing the assumptions used for the valuation
    parameters = Column(Text, nullable=True)  # JSON string containing the parameters used for the valuation
    file_path = Column(String, index=True, unique=True)  # Path to the file containing the valuation report | CSV or Excel file
    #<stock_symbol>_<valuation_method>_<valuation_date>.csv
    

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete='CASCADE'))
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete='CASCADE'))
    transaction_type = Column(Enum('BUY', 'SELL', 'DIVIDEND','STOCK_SPLIT', name='transaction_types'))
    transaction_date = Column(Date)
    quantity = Column(Integer)
    price = Column(Float)
    fees = Column(Float)
    

    @validates('price')
    def validate_price(self, key, price):
        if self.transaction_type in ('DIVIDEND', 'STOCK_SPLIT'):
            return 0  # Set price to zero for DIVIDEND and STOCK_SPLIT transactions
        return price
