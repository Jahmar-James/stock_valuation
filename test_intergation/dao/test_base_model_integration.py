# # test/dao/test_base_model_integration.pys

# import pytest
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import sessionmaker

# from app.dao.models.base import BaseModel

# # Define a test model
# class TestModel(BaseModel):
#     __tablename__ = 'test_model'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)

# # Set up a test database connection (replace with your test database URI)
# DATABASE_URI = "sqlite:///:memory:"
# engine = create_engine(DATABASE_URI)

# # Create a session for the test
# Session = sessionmaker(bind=engine)

# @pytest.fixture(scope='function')
# def session():
#     BaseModel.metadata.create_all(engine)
#     s = Session()
#     yield s
#     s.close()
#     BaseModel.metadata.drop_all(engine)

# def test_versioning(session):
#     instance = TestModel(name="Original")
#     session.add(instance)
#     session.commit()

#     assert instance.versions.count() == 1

#     instance.name = "Modified"
#     session.add(instance)
#     session.commit()

#     assert instance.versions.count() == 2
