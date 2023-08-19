# app/dao/models/historical_metrics.py
from sqlalchemy import Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import BaseORMVersioned

class HistoricalMetrics(BaseORMVersioned):
    """
    Quarterly key historical metrics for a stock
    """
    __tablename__ = "historical_metric"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"))
    date: Mapped[Date] = mapped_column(Date)
    revenue: Mapped[float] = mapped_column(Float)
    net_income: Mapped[float] = mapped_column(Float)
    price_to_earnings: Mapped[float] = mapped_column(Float)
    price_to_book: Mapped[float] = mapped_column(Float)
    price_to_sales: Mapped[float] = mapped_column(Float)
    price_to_cashflow: Mapped[float] = mapped_column(Float)
    price_to_earnings_growth: Mapped[float] = mapped_column(Float)
    dividend_yield: Mapped[float] = mapped_column(Float)
    payout_ratio: Mapped[float] = mapped_column(Float)
    shares_outstanding: Mapped[float] = mapped_column(Float)
    market_cap: Mapped[float] = mapped_column(Float)
    enterprise_value: Mapped[float] = mapped_column(Float)
    enterprise_value_to_revenue: Mapped[float] = mapped_column(Float)
    return_on_equity: Mapped[float] = mapped_column(Float)
    return_on_investment: Mapped[float] = mapped_column(Float)

    # Relationships
    # one-to-many -> (A Stock) - has - (Historical Metrics)
    stock: Mapped["Stock"] = relationship("Stock", back_populates="historical_metrics")

    def __repr__(self):
        return (f"<HistoricalMetrics(id={self.id}, stock_id={self.stock_id}, date={self.date}, "
                f"Market_cap{self.market_cap})>")
