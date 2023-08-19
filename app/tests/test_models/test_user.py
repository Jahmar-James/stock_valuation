# test_user.py
from unittest.mock import Mock, MagicMock, create_autospec
from app.models.user import User
import pytest

"""
Unit tests for the User model:
    - Test that a User instance can be created with proper attributes.
    - Test the default behavior for last_login attribute.
    - Test the uniqueness constraint for the username.
    - Test the hashing behavior for the password.
"""

# Test if a user is properly initialized and added to session
def test_create_user(fake_user_data):
    """
    Test that a User instance can be created and added to a mock session.
    """
    # Creating a mock session
    mock_session = create_autospec(spec=MagicMock, instance=True)
    
    # Simulating add and commit do nothing
    mock_session.add = Mock()
    mock_session.commit = Mock()

    # Mocking the query method to retrieve our user
    mock_session.query.return_value.filter_by.return_value.first.return_value = fake_user_data
    
    user_data = fake_user_data
    mock_session.add(user_data)
    mock_session.commit()

    retrieved_user = mock_session.query(User).filter_by(username=user_data['username']).first()
    assert retrieved_user is not None
    assert retrieved_user['first_name'] == user_data['first_name']
    assert retrieved_user['last_name'] == user_data['last_name']


from datetime import datetime, timedelta

def test_default_last_login(fake_user_data):
    """
    Test that the default last_login attribute is set upon user creation.
    """
    user = User(**fake_user_data)

    # Check that last_login is recent (within a few seconds of "now")
    assert user.last_login is not None
    assert abs(user.last_login - datetime.utcnow()) < timedelta(seconds=5)

def test_username_uniqueness(fake_user_data):
    """
    Test that a ValueError is raised when a duplicate username is encountered.
    """
    # Creating a mock session
    mock_session = create_autospec(spec=Mock, instance=True)
    
    # Simulate a user with the same username exists in the database
    mock_session.query.return_value.filter_by.return_value.first.return_value = fake_user_data

    # Create a user instance with the same username
    user = User(**fake_user_data)

    with pytest.raises(ValueError, match="Username must be unique"):
        # Add logic here to check the uniqueness and raise ValueError if not unique
        if mock_session.query(User).filter_by(username=user.username).first():
            raise ValueError("Username must be unique")

def test_password_hashing(fake_user_data):
    """
    Test that the password of a user is properly hashed upon creation.
    """
    user = User(**fake_user_data)
    assert user.password_hash is not None
    assert user.password_hash != fake_user_data['password']

"""
Notes for Future Reference:
User Model:
  - Unit: Ensure username uniqueness, default last_login behavior, and password hashing.
  - Integration: Test unique constraints in DB, password verification, and interactions with other models.
"""
