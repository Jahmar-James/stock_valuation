# app/tests/test_models/test_transaction.py
import pytest
from app.dao.models import Transaction
from app.tests.fixtures.conftest import fake_transaction_data_list
from collections import namedtuple

"""
Unit tests for the Transaction model:
    - Test that a Transaction instance can be created with proper attributes.
    - Test the price validation logic.
"""

def test_create_transaction(fake_transaction_data_list):
    """
    Test that a Transaction instance can be created with proper attributes.
    """
    for transaction_data in fake_transaction_data_list:
        transaction = Transaction(**transaction_data)

        # Check attributes
        assert transaction.stock_id == transaction_data['stock_id']
        assert transaction.portfolio_id == transaction_data['portfolio_id']
        assert transaction.transaction_type == transaction_data['transaction_type']
        assert transaction.quantity == transaction_data['quantity']
        assert transaction.price == transaction_data.get('price', 0)  # Default to 0 for dividend/stock_split
        assert transaction.fees == transaction_data['fees']

        # Check DB generated attributes - id should be None unless persisted
        assert transaction.id is None

        # Check relationships - these should be empty initially
        assert transaction.portfolio is None

def test_price_validation_for_dividend_and_stock_split():
    """
    Test that the price for 'DIVIDEND' and 'STOCK_SPLIT' transactions is set to 0.
    """
    transaction_of_dividend =  Transaction(transaction_type='DIVIDEND', price=10.5)  # Pass a non-zero price
    transaction_of_stock_split = Transaction(transaction_type='STOCK_SPLIT', price=15.5)  # Pass a non-zero price
    
    assert transaction_of_dividend.price == 0
    assert transaction_of_stock_split.price == 0

Transaction_test_case = namedtuple('TestCase', ['attributes', 'description', 'should_raise'])

@pytest.mark.parametrize(
    "transaction_min_test", [
        Transaction_test_case({"transaction_type": "BUY", "quantity": 10}, "Minimum required attributes", False), # Minimum required attributes
        Transaction_test_case({"transaction_type": "BUY"}, "Missing 'quantity'", True), # Missing 'quantity'
        Transaction_test_case({"quantity": 10}, "Missing 'transaction_type'", True) # Missing 'transaction_type'
    ]
)
def test_transaction_creation_with_minimal_attributes(transaction_min_test):
    """Test that Transaction instance can be created with minimal attributes."""
    if transaction_min_test.should_raise:
        with pytest.raises(AssertionError):
            transaction = Transaction(**transaction_min_test.attributes)
            
            # Assert that 'transaction_type' and 'quantity' are not None
            assert transaction.transaction_type is not None
            assert transaction.quantity is not None
    else:
        transaction = Transaction(**transaction_min_test.attributes)
        
        # Assert that 'transaction_type' and 'quantity' are not None
        assert transaction.transaction_type is not None
        assert transaction.quantity is not None
        
"""
Notes for Future Reference:
Transaction Model:
    - Unit: Only necessary unit tests are for attribute initialization and class method of validation.
    - Integration: Test interactions with other models, especially UserPortfolio and Stock.
     CRUD operations and behaviors should be tested in repository and service layers.
"""