# app/tests/test_models/test_user.py
from app.dao.models.user import User

from app.tests.fixtures.conftest import fake_user_data, mocked_user
from datetime import datetime

"""
Unit tests for the User model:
    - Test that a User instance can be created with proper attributes.
    - Test the default behavior for last_login attribute.
"""

def test_create_user(mocked_user, fake_user_data):
    """
    Test that a User instance can be created with proper attributes.
    """

    assert mocked_user.first_name == fake_user_data['first_name']
    assert mocked_user.last_name == fake_user_data['last_name']
    assert mocked_user.username == fake_user_data['username']
    assert mocked_user.hashed_password == fake_user_data['hashed_password']
     
    # Check DB generated attributes - id, last_login should be None unless mocked
    assert mocked_user.id is None
    assert mocked_user.configuration is None
    
        # mocked DB generated attributes
    assert mocked_user.permission == 'USER'
    assert isinstance(mocked_user.last_login,datetime)
    
    # No portfolios as its a relationship
    
"""
Notes for Future Reference:
User Model:
  - Unit: Only necessary unit tests are for attribute initialization and default behaviors.
  - Integration: Test unique constraints in DB, interactions with other models, and related CRUD operations. 
    CRUD operations and behaviors such as password verification should be tested in repository and service layers.
"""
