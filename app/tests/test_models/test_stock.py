# test_stock.py
import pytest
from unittest.mock import Mock, create_autospec
from sqlalchemy.exc import IntegrityError

"""
Unit tests for the Stock model:
    - Test that a Stock instance can be created with just a ticker_symbol.
    - Test the uniqueness of the ticker_symbol.
    - Test the behavior of appending and clearing relationships like historical_prices, dividends, etc.
"""
# Test if a stock is properly initialized
def test_stock_initialization(mock_stock_aapl):
    assert mock_stock_aapl.ticker_symbol == "AAPL"
    assert mock_stock_aapl.company_name == "Apple Inc."

# Test appending a stock to a sector
def test_append_stock_to_sector(mock_stock_aapl, mock_sector):
    mock_sector.stocks.append(mock_stock_aapl)
    assert mock_stock_aapl in mock_sector.stocks

# Test unique constraint on stock ticker_symbol
def test_unique_stock_ticker(mock_stock_msft):
    mock_session = create_autospec(spec=Mock, instance=True)
    
    mock_session.query().filter().first.return_value = mock_stock_msft
    mock_session.add(mock_stock_msft)

    with pytest.raises(IntegrityError, match="UNIQUE constraint failed: stock.ticker_symbol"):
        mock_session.commit()



"""
Notes for Future Reference:
Stock Model:
  - Unit: Ensure ticker_symbol uniqueness and manage relationships.
  - Integration: Test unique constraints in DB, relationship mappings, and cascading behaviors.
"""