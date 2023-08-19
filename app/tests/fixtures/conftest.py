# app/test/fixture/conftest.py
import pytest
from faker import Faker
from unittest.mock import Mock

fake = Faker([
    'en_US',     # United States
    'en_CA',     # Canada
    'ko_KR',     # Korea
    'ja_JP',     # Japan
    'zh_CN',     # China
    'fr_FR',     # France
    'ar_AE',     # UAE
    'de_DE',     # Germany
    'en_ZA',     # South Africa
])

@pytest.fixture
def fake_user_data():
    return {
        "username": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "hashed_password": fake.password()
    }

@pytest.fixture
def mock_stock_aapl():
    return Mock(ticker_symbol="AAPL", company_name="Apple Inc.")

@pytest.fixture
def mock_stock_msft():
    return Mock(ticker_symbol="MSFT", company_name="Microsoft Corporation")

@pytest.fixture
def mock_stock_googl():
    return Mock(ticker_symbol="GOOGL", company_name="Alphabet Inc.")

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