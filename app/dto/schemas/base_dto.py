from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel, PrivateAttr, ConfigDict

class BaseModelRepresentation(PydanticBaseModel):
    """Pydantic base model for data representation."""
    model_config = ConfigDict(from_attributes=True) # orm_mode is now from_attributes
    _processed_at: datetime = PrivateAttr(default_factory=datetime.utcnow)
    
    def __repr__(self):
        return f'DTO: <{self.__class__.__name__}>'