# app/dao/models/stock_sector.py

from sqlalchemy import Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import BaseORMVersioned

stock_sector_association = Table(
    'stock_sector', 
    BaseORMVersioned.metadata,
    mapped_column('stock_id', Integer, ForeignKey('stocks.id')),
    mapped_column('sector_id', Integer, ForeignKey('sector.id'))
)

class Stock(BaseORMVersioned):
    """
    Represents a stock in the database. 
    - DAO (Data Access Object) 

    Attributes:
        id (int): The auto-incrementing primary key for the stock.
        ticker_symbol (str): The ticker symbol of the stock (e.g., AAPL).
        company_name (str): The name of the company that the stock belongs to.
        historical_prices (list[HistoricalPrice]): The historical prices of the stock.
        dividends (list[Dividend]): The dividends of the stock.
        sectors (list[Sector]): The sectors that the stock belongs to.
        historical_metrics (list[HistoricalMetrics]): The historical metrics of the stock.
        holding (list[Holding]): The holdings of the stock (e.g. quantity, purchase date, etc. )

    """
    __tablename__ = "stocks"

   # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticker_symbol: Mapped[str] = mapped_column(String, index=True, unique=True)
    company_name: Mapped[str] = mapped_column(String)

    # Relationships
    # one-to-many -> (A Stock) - has - (Historical Prices)
    historical_prices: Mapped["HistoricalPrice"] = relationship("HistoricalPrice", back_populates="stock")
    # one-to-many -> (A Stock) - has - (Dividends)
    dividends: Mapped["Dividend"] = relationship("Dividend", back_populates="stock")
    # many-to-many -> (A Stock) - belongs to - (Sectors)
    sectors: Mapped["Sector"] = relationship("Sector", secondary=stock_sector_association, back_populates="stocks")
    # one-to-many -> (A Stock) - has - (Historical Metrics)
    historical_metrics: Mapped["HistoricalMetrics"] = relationship("HistoricalMetrics", back_populates="stock")
    # one-to-many -> (A Stock) - has - (Holdings)
    holding: Mapped["Holding"] = relationship("Holding", back_populates="stock")

    def __repr__(self):
        return f"<Stock(id={self.id}, ticker_symbol={self.ticker_symbol}, company_name={self.company_name})>"

class Sector(BaseORMVersioned):
    """
    Represents a sector in the database.
    - DAO (Data Access Object)

    Attributes:
        id (int): The auto-incrementing primary key for the sector.
        name (str): The name of the sector.
        description (str): The description of the sector.
        stocks (list[Stock]): The stocks that belong to the sector.

    """
    __tablename__ = "sector"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String)

    # Relationships
    # many-to-many -> (A Sector) - contains - (Stocks)
    stocks: Mapped["Stock"] = relationship("Stock", secondary=stock_sector_association, back_populates="sectors")

    def __repr__(self):
        return f"<Sector(id={self.id}, name={self.name}, description={self.description})>"