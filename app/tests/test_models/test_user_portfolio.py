# app/tests/test_models/test_user_portfolio.py
import pytest
from unittest.mock import Mock
from app.dao.models import UserPortfolio
from app.tests.fixtures.conftest import fake_user_data, mocked_user, fake_portfolio_data_real, fake_portfolio_data_paper
from datetime import datetime

"""
Unit tests for the UserPortfolio model:
    - Test that a UserPortfolio instance can be created with proper attributes.
    - Test the default behavior for creation_date attribute.
"""
def test_create_real_user_portfolio(mocked_user, fake_portfolio_data_real):
    """
    Test that a UserPortfolio instance can be created with proper attributes.
    """
    portfolio = UserPortfolio(
        user=mocked_user,
        name=fake_portfolio_data_real['name'],
        description=fake_portfolio_data_real['description'],
        type=fake_portfolio_data_real['type']
    )

    # Check attributes
    assert portfolio.user == mocked_user
    assert portfolio.name == fake_portfolio_data_real['name']
    assert portfolio.description == fake_portfolio_data_real['description']
    assert portfolio.type == fake_portfolio_data_real['type']

    # Check DB generated attributes - id should be None unless mocked
    assert portfolio.id is None
    assert portfolio.creation_date is None

    # Check relationships - these should be empty initially unless mocked
    assert not portfolio.transactions
    assert not portfolio.holdings
    
def test_create_paper_portfolio(mocked_user, fake_portfolio_data_paper):
    """
    Test that a paper UserPortfolio instance can be created with proper attributes.
    """
    portfolio = UserPortfolio(**fake_portfolio_data_paper)
    
    # Check attributes
    assert portfolio.user == mocked_user
    assert portfolio.name == fake_portfolio_data_paper['name']
    assert portfolio.description == fake_portfolio_data_paper['description']


"""
Notes for Future Reference:
UserPortfolio Model:
  - Unit: Only necessary unit tests are for attribute initialization and default behaviors.
  - Integration: Test interactions with other models, especially User, Transaction, and Holding.
    CRUD operations and behaviors should be tested in repository and service layers.
"""
