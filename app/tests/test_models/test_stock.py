# app/tests/test_models/test_stock.py
from app.dao.models import Stock
from app.tests.fixtures.conftest import fake_stock_data_list

"""
Unit tests for the Stock model:
    - Test that a Stock instance can be created with proper attributes.
"""

def test_create_stock(fake_stock_data_list):
    """
    Test that a Stock instance can be created with proper attributes.
    """
    for stock_data in fake_stock_data_list:
        stock = Stock(**stock_data)

        # Check attributes
        assert stock.ticker_symbol == stock_data['ticker_symbol']
        assert stock.company_name == stock_data['company_name']

        # Check DB generated attributes - id should be None unless persisted
        assert stock.id is None

        # Check relationships - these should be empty initially
        assert not stock.historical_prices
        assert not stock.dividends
        assert not stock.sectors
        assert not stock.historical_metrics
        assert not stock.holding
    
"""
Notes for Future Reference:
Stock Model:
  - Unit: Only necessary unit tests are for attribute initialization and relationships.
  - Integration: Test associations with other models, especially Sector, HistoricalPrice, Dividend, etc.
    CRUD operations and behaviors should be tested in repository and service layers.
"""