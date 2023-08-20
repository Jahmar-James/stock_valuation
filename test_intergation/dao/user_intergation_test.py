# test/dao/models/user_unit_test.py
import sys
sys.path.insert(0, "O:\\Documents\\Python_Projects\\stock_valuation")

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,configure_mappers
from sqlalchemy_continuum import make_versioned
from config import Config
from app.dao.models.user import User

# from app.dao.models.base import BaseModel
# from faker import Faker

# fake = Faker()

# def create_fake_user():
#     return User(
#         username=fake.user_name(),
#         first_name=fake.first_name(),
#         last_name=fake.last_name(),
#         hashed_password=fake.password()
#     )

# engine = create_engine(Config.DB_TEST)
# SessionLocal = sessionmaker(bind=engine)

# @pytest.fixture(scope="module")
# def setup_database():
#     # Create the tables
#     make_versioned()
#     from app.dao.models import UserPortfolio, Transaction, Holding, Dividend, Configuration, ValuationModel, Stock, Sector, HistoricalPrice, HistoricalMetrics, Document
#     configure_mappers()
    
#     yield  # this is where the testing happens    
#     # Drop the tables
#     BaseModel.metadata.drop_all(bind=engine)
    
# @pytest.fixture(scope="module")
# def session(setup_database):
#     """Provide a session for testing, rollback transactions after each test."""
#     session = SessionLocal(autoflush=False)

#     session.begin_nested()  # start a new transaction
#     yield session  # this is where the testing happens
#     session.rollback()
#     session.close()

# def test_create_user(session):
#    # Create a fake user using our utility function
#     user = create_fake_user()
    
#     session.add(user)
#     session.flush()
#     session.commit()
    
#     # Now, retrieve the user to ensure they were properly added
#     retrieved_user = session.query(User).filter_by(username=user.username).first()
#     assert retrieved_user is not None
#     assert retrieved_user.first_name == user.first_name
#     assert retrieved_user.last_name == user.last_name

# # Add more tests as needed, e.g., for relationships and custom operations.

# # TODO: Test relationships. You'll need to import and create related models in the test.
# # Ensure that cascading behaviors, back_populates, and other relationship aspects work correctly.

# # TODO: Test any custom queries or operations associated with the User model.
