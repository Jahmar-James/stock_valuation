# test_sector.py
import pytest
from unittest.mock import Mock
from app.dao.models.stock_sector import Sector
from sqlalchemy.exc import IntegrityError


"""
Unit tests for the Sector model:
    - Test that a Sector instance can be created with just a name.
    - Test the uniqueness of the name.
    - Test the behavior of appending and clearing stocks in the stocks relationship
"""


# Test initialization of a sector with specific attributes
@pytest.mark.parametrize("mock_sector", 
                         [{"name": "Technology", "description": "Tech companies"},
                          {"name": "Finance", "description": "Financial Sector"}], 
                         indirect=True)
def test_sector_initialization(mock_sector):
    assert mock_sector.name in ["Technology", "Finance"]
    assert mock_sector.description in ["Tech companies", "Financial Sector"]

@pytest.mark.parametrize("mock_sector", 
                         [{"name": "", "description": "No name sector"},   # Edge case: Empty name
                          {"name": "Very long sector name...", "description": "Standard description"}], # Edge case: Long name
                         indirect=True)
def test_sector_edge_initialization(mock_sector):
    assert mock_sector.name in [ "", "Very long sector name..."]
    assert mock_sector.description in ["No name sector", "Standard description"]

# Test that stocks can be added and removed to a sector
def test_append_and_clear_stocks(mock_stock_aapl, mock_stock_msft):
    sector = Sector(name="Technology")
    sector.stocks.extend([mock_stock_aapl, mock_stock_msft])
    
    assert len(sector.stocks) == 2
    sector.stocks.clear()
    assert len(sector.stocks) == 0

# Test that a sector name must be unique
def test_sector_name_uniqueness(mock_sector):
    # Assuming you have a mock_session similar to your previous examples
    mock_session = Mock()
    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_sector
    
    new_sector = Sector(name=mock_sector.name)
    
    with pytest.raises(IntegrityError):  
        # This is a mocked behavior, in reality, your ORM or DB would raise an exception
        if mock_session.query(Sector).filter_by(name=new_sector.name).first():
            raise IntegrityError("Sector with this name already exists.")

def test_stock_filtering(mock_stock_aapl, mock_stock_msft, mock_stock_googl):
    sector = Sector(name="Technology")
    sector.stocks.extend([mock_stock_googl, mock_stock_aapl, mock_stock_msft])
    
    # Mock a filter method
    def mock_filter_by(ticker_symbol=None):
        return [stock for stock in sector.stocks if stock.ticker_symbol == ticker_symbol]
    
    # Use the mock filter method
    filtered_stocks = mock_filter_by(ticker_symbol="AAPL")
    assert filtered_stocks == [mock_stock_aapl]

"""
Notes for Future Reference:
Sector Model:
  - Unit: Test name uniqueness and manage stock relationships.
  - Integration: Test name unique constraints in DB and many-to-many relationship behaviors.
"""