# app/tests/test_models/test_base_model.py
from unittest.mock import patch, Mock
from app.dao.models.base import BaseORMVersioned

"""
Unit tests for the BaseORMVersioned:
    - Test the `__repr__` method of the BaseORMVersioned for consistent representation.
"""

@patch("app.dao.models.base.make_versioned")
@patch("app.dao.models.base.registry")
def test_base_model_repr(mock_registry, mock_make_versioned):
    """
    Test the representation method (__repr__) for BaseORMVersioned.
    """
    # Mocking the Base generation process
    mock_registry_instance = Mock()
    mock_registry.return_value = mock_registry_instance
    mock_registry_instance.generate_base.return_value = Mock()

    # Create a dummy class to represent a concrete model that inherits from BaseORMVersioned
    class DummyModel(BaseORMVersioned):
        __abstract__ = True
        __tablename__ = "dummy_table_test"

    instance = DummyModel()
    instance.id = 1

    # Test the __repr__ method
    assert repr(instance) == "ORM:<DummyModel 1>"
    assert str(instance) == "ORM:<DummyModel 1>"
    assert instance.__class__.__name__ == "DummyModel"

"""
Notes for Future Reference:
BaseORMVersioned:
  - Unit: Ensure consistent representation using the __repr__ method.
  - Integration: Test versioning behavior in a real database environment.
"""