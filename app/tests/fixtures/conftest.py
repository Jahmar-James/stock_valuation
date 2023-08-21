# app/test/fixture/conftest.py
import pytest
from faker import Faker
from unittest.mock import Mock
from datetime import datetime
from app.dao.models.user import User


fake = Faker([
    'en_US',     # United States
    'en_CA',     # Canada
    'ko_KR',     # Korea
    'ja_JP',     # Japan
    'zh_CN',     # China
    'fr_FR',     # France
    'ar_AE',     # UAE
    'de_DE',     # Germany
])



class MockedUser(User):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        if self.permission is None:
            self.permission = 'USER'
    
    @property
    def last_login(self):
        if not hasattr(self, "_last_login"):
            self._last_login = datetime.utcnow()
        return self._last_login

    @last_login.setter
    def last_login(self, value):
        self._last_login = value
        
@pytest.fixture
def fake_user_data():
    return {
        "username": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "hashed_password": fake.password()
    }

@pytest.fixture
def mocked_user(fake_user_data):
    user = MockedUser(**fake_user_data)
    return user 

@pytest.fixture
def fake_portfolio_data_real(mocked_user):
    """Generate fake data for a real portfolio."""
    return {
        "user": mocked_user,
        "name": fake.company_suffix(),
        "description": fake.catch_phrase(),
        "type": "real"
    }

@pytest.fixture
def fake_portfolio_data_paper(mocked_user):
    """Generate fake data for a paper portfolio."""
    return {
        "user": mocked_user,
        "name": fake.company_prefix(),
        "description": fake.bs(),  # Generates a random "buzzword"
        "type": "paper"
    }

def mock_transaction(id=None):
    transaction = Mock()
    transaction.id = id if id is not None else fake.random_int()
    return transaction

def mock_holding(id=None):
    holding = Mock()
    holding.id = id if id is not None else fake.random_int()
    return holding

def _mock_transaction(id=None):
    """
    Mock a transaction.
    """
    return {
        "id": id if id else fake.uuid4(),  # Assign a UUID if id is not provided.
        "user": mocked_user,
        "asset": fake.company_suffix(),   # Perhaps better to have another method to mock assets.
        "quantity": fake.random_int(min=1, max=1000),
        "transaction_date": fake.date_this_decade(),
        "transaction_type": fake.random_element(elements=("buy", "sell")),
        "price_per_unit": fake.random_number(digits=4)  # Generating a random price.
    }

@pytest.fixture
def mocked_transaction():
    return _mock_transaction()



@pytest.fixture
def fake_stock_data_aapl():
    return {"ticker_symbol": "AAPL", "company_name": "Apple Inc."}

@pytest.fixture
def fake_stock_data_msft():
    return {"ticker_symbol": "MSFT", "company_name": "Microsoft Corporation"}

@pytest.fixture
def fake_stock_data_googl():
    return {"ticker_symbol": "GOOGL", "company_name": "Alphabet Inc."}

@pytest.fixture
def fake_stock_data_list():
    """Generate a list of mock stock data for testing purposes."""
    return [
        {"ticker_symbol": "AAPL", "company_name": "Apple Inc."},
        {"ticker_symbol": "MSFT", "company_name": "Microsoft Corporation"},
        {"ticker_symbol": "GOOGL", "company_name": "Alphabet Inc."}
    ]
    
@pytest.fixture
def fake_sector_data_list():
    """Generate a list of mock sector data for testing purposes."""
    return [
        {"name": "Technology", "description": "Tech companies like Apple, Microsoft, etc."},
        {"name": "Finance", "description": "Banks and financial institutions."},
        {"name": "Healthcare", "description": "Pharmaceuticals, hospitals, etc."}
    ]
    
@pytest.fixture
def fake_transaction_data_list():
    """Generate a list of mock transaction data for testing purposes."""
    return [
        {"stock_id": 1, "portfolio_id": 1, "transaction_type": "BUY", "quantity": 10, "price": 150.0, "fees": 5.0},
        # Add other types and data as necessary...
    ]


@pytest.fixture
def mock_sector(request):
    return Mock(name=request.param.get("name", "Default Sector Name"), 
                description=request.param.get("description", "Default Description"))

@pytest.fixture
def mock_historical_price():
    return Mock()

@pytest.fixture
def mock_dividend():
    return Mock()