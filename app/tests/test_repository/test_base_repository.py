# app/tests/test_repository/test_base_repository.py

from app.dao.repository.base_repository import BaseRepository
from app.dao.models.base import BaseORMVersioned
from sqlalchemy import Integer, String, DateTime, Column
from sqlalchemy.exc import SQLAlchemyError
import pytest
from unittest.mock import Mock, patch, MagicMock,create_autospec 
from sqlalchemy.orm import Session

"""
Unit tests for the BaseRepository class:
    - Test that an entity can be added successfully to the session.
    - Test that adding an invalid entity raises an error and returns the expected result.

Notes for Future Reference:
BaseRepository class:
  - Unit: Testing is focused on mocking the SQLAlchemy session and ensuring that methods interact with it correctly.
  - Integration: Test the actual CRUD operations against a real database, possibly an in-memory SQLite for simplicity.
""" 

class MockedORM(BaseORMVersioned):
    __tablename__ = "mock_entity"

    id = Column(Integer, primary_key=True, index=True)
    attribute = Column(String)
    date = Column(DateTime)
    number = Column(Integer)
    
@pytest.fixture
def mocked_entity():
    """Provides a mocked entity instance."""
    entity_instance = MockedORM()
    entity_instance.id = 1
    entity_instance.attribute = "mock_value"
    entity_instance.date = "2021-01-01"
    entity_instance.number = 1
    return entity_instance

@pytest.fixture(params=[True, False], ids=['found', 'not_found'])
def mocked_result(request, mocked_entity):
    """Provides a mocked result based on the presence or absence of an entity."""
    mock_scalars = Mock()
    
    # Determine if the entity is found or not based on the parameter.
    entity_value = mocked_entity if request.param else None
    mock_scalars.first.return_value = entity_value

    # Create a result mock to return our mock_scalars.
    result = Mock()
    result.scalars.return_value = mock_scalars
    
    return result

@pytest.fixture
def mock_provide_session(mocked_result):
    """Mocks the provide_session context manager."""
    with patch("app.dao.repository.base_repository.provide_session") as mock:
        mock_session = create_autospec(Session)
        
        mock_session.execute.return_value = mocked_result

        mock.return_value.__enter__.return_value = mock_session
        yield mock_session
    mock.return_value.__exit__.return_value = None
    
@pytest.fixture
def mocked_entities_list(mocked_entity):
    """Provides a list of mocked entities."""
    return [mocked_entity for _ in range(3)]

@pytest.fixture
def mock_base_repository():
    """Mocks the BaseRepository with a mocked model."""
    repository = BaseRepository(model=MockedORM)
    return repository

def test_create_valid_entity_succeeds(mock_provide_session, mocked_entity, mock_base_repository):
    mock_provide_session.add.return_value = None
    mock_provide_session.flush.return_value = None

    result, entity_id = mock_base_repository.create_entity(mocked_entity)
    # Check the return values of a successful create_entity call
    assert result == True
    assert entity_id == 1
    # Check the correct session methods were called
    mock_provide_session.add.assert_called_once_with(mocked_entity)
    mock_provide_session.flush.assert_called_once()

def test_create_invalid_entity_fails(mock_provide_session, mocked_entity, mock_base_repository):
    mock_provide_session.flush.side_effect = SQLAlchemyError("Mocked SQLAlchemy Error")

    result, entity_id = mock_base_repository.create_entity(mocked_entity)
    # Check the return values of a successful create_entity call
    assert result == False
    assert entity_id == -1
    
def test_retrieve_entity_by_id(mock_provide_session, mocked_entity, mock_base_repository, mocked_result):
    """Test the retrieve_entity_by_id function."""
    retrieved_entity = mock_base_repository.retrieve_entity_by_id(1)

    expected_entity = mocked_result.scalars().first()

    # Check if the returned entity is as expected
    assert retrieved_entity == expected_entity
    
    if retrieved_entity:
        assert retrieved_entity.id == expected_entity.id
        assert retrieved_entity.attribute == expected_entity.attribute
    
    # Ensure the correct SQL statement was executed
    mock_provide_session.execute.assert_called_once()
    
@pytest.mark.parametrize("entity_present", [True, False], ids=['found', 'not_found'])
def test_retrieve_entity_by_attribute(mock_provide_session, mocked_entity, mock_base_repository, entity_present):
    """Test the retrieve_entity_by_attribute function for both found and not found scenarios."""
    
    attribute_to_search = MockedORM.attribute
    value_to_search = mocked_entity.attribute if entity_present else "non_existent_value"
    
    # Mock the session's execute method based on entity_present
    mock_result = Mock()
    mock_scalars = Mock()
    mock_scalars.first.return_value = mocked_entity if entity_present else None
    mock_result.scalars.return_value = mock_scalars
    mock_provide_session.execute.return_value = mock_result

    retrieved_entity = mock_base_repository.retrieve_entity_by_attribute(attribute_to_search, value_to_search)

    # Check if the returned entity is as expected
    if entity_present:
        assert retrieved_entity == mocked_entity
        mock_provide_session.expunge.assert_called_once_with(mocked_entity)
    else:
        assert retrieved_entity is None
        mock_provide_session.expunge.assert_not_called()

    # Ensure the correct SQL statement was executed
    mock_provide_session.execute.assert_called_once()


    

    


