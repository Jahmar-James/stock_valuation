# app/tests/test_base_model.py
from unittest.mock import patch, Mock
from app.dao.models.base import BaseModel

"""
Unit tests for the BaseModel:
    - Test the `__repr__` method of the BaseModel for consistent representation.
"""

@patch("app.dao.models.base.make_versioned")
@patch("app.dao.models.base.registry")
def test_base_model_repr(mock_registry, mock_make_versioned):
    """
    Test the representation method (__repr__) for BaseModel.
    """
    # Mocking the Base generation process
    mock_registry_instance = Mock()
    mock_registry.return_value = mock_registry_instance
    mock_registry_instance.generate_base.return_value = Mock()

    # Create a dummy class to represent a concrete model that inherits from BaseModel
    class DummyModel(BaseModel):
        pass

    instance = DummyModel()
    instance.id = 1

    # Test the __repr__ method
    assert repr(instance) == "<DummyModel 1>"

"""
Notes for Future Reference:
BaseModel:
  - Unit: Ensure consistent representation using the __repr__ method.
  - Integration: Test versioning behavior in a real database environment.
"""