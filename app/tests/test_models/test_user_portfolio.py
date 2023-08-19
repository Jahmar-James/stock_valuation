# test_user_portfolio.py
import pytest
from unittest.mock import Mock
from app.dao.models import User, UserPortfolio
from app.tests.conftest import fake

"""
Unit tests for the UserPortfolio model:
    - Test relationships (e.g., user association).
    - Test the behavior of appending and clearing transactions and holdings.
"""

# Helper functions to generate mock objects for clarity
@pytest.fixture
def mock_user(fake_user_data):
    mock_user_obj = Mock(spec=User)
    for key, value in fake_user_data.items():
        setattr(mock_user_obj, key, value)
    return mock_user_obj

@pytest.fixture
def real_portfolio(mock_user):
    return UserPortfolio(name="Test Portfolio", type="real", user=mock_user)

@pytest.fixture
def paper_portfolio(mock_user):
    return UserPortfolio(name="Sample Portfolio", type="paper", user=mock_user)

def mock_transaction(id=None):
    transaction = Mock()
    transaction.id = id if id is not None else fake.random_int()
    return transaction

def mock_holding(id=None):
    holding = Mock()
    holding.id = id if id is not None else fake.random_int()
    return holding

def test_user_relationship(real_portfolio, mock_user, fake_user_data):
    """
    Test the association between user and portfolio.
    """
    assert real_portfolio.user is mock_user
    assert real_portfolio.user.username == fake_user_data["username"]

def test_add_transaction_to_portfolio(real_portfolio):
    """
    Test appending a transaction to a portfolio.
    """

    transaction = mock_transaction()
    real_portfolio.transactions.append(transaction)

    assert transaction in real_portfolio.transactions

def test_add_holding_to_portfolio( paper_portfolio):
    """
    Test appending a holding to a portfolio.
    """
    holding = mock_holding(id=1)
    paper_portfolio.holdings.append(holding)

    assert holding in paper_portfolio.holdings
    assert paper_portfolio.holdings[0].id == 1

    new_holding = mock_holding()
    paper_portfolio.holdings.append(new_holding)
    assert paper_portfolio.holdings[1] == new_holding
    # Double check that the old holding is still there
    assert holding in paper_portfolio.holdings
    assert new_holding in paper_portfolio.holdings

def test_clear_transactions_from_portfolio(real_portfolio):
    """
    Test clearing transactions from a portfolio.
    """
    real_portfolio.transactions = [mock_transaction(), mock_transaction()]
    real_portfolio.transactions.clear()

    assert len(real_portfolio.transactions) == 0

def test_clear_holdings_from_portfolio(paper_portfolio):
    """
    Test clearing holdings from a portfolio.
    """
    paper_portfolio.holdings = [mock_holding(), mock_holding()]
    paper_portfolio.holdings.clear()

    assert len(paper_portfolio.holdings) == 0

"""
Notes for Future Reference:
UserPortfolio Model:
  - Unit: Ensure proper management and association of users, transactions, and holdings.
  - Integration: Test real interactions with the database, and the cascading behaviors.
"""