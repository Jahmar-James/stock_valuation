from datetime import datetime
from schemas.base_dto import PydanticBaseModel

class UserDataTransfer(PydanticBaseModel):
    """ Model for transferring User data. (DTO))"""
    name: str
    age: int
    email: str

# User from ORM
class UserFromDB(UserDataTransfer):
    """User data representation from ORM."""
    id: int
    created_at: datetime
    updated_at: datetime
