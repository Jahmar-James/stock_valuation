# app/tests/test_models/test_sector.py
from app.dao.models import Sector
from app.tests.fixtures.conftest import fake_sector_data_list

"""
Unit tests for the Sector model:
    - Test that a Sector instance can be created with proper attributes.
"""

def test_create_sector(fake_sector_data_list):
    """
    Test that a Sector instance can be created with proper attributes.
    """
    for sector_data in fake_sector_data_list:
        sector = Sector(**sector_data)

        # Check attributes
        assert sector.name == sector_data['name']
        assert sector.description == sector_data['description']

        # Check DB generated attributes - id should be None unless persisted
        assert sector.id is None

        # Check relationships - these should be empty initially
        assert not sector.stocks
    
"""
Notes for Future Reference:
Sector Model:
  - Unit: Only necessary unit tests are for attribute initialization and relationships.
  - Integration: Test associations with other models, especially Stock.
    CRUD operations and behaviors should be tested in repository and service layers.
"""