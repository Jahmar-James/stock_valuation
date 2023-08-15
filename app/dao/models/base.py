# app/dao/models/base.py
from sqlalchemy.orm import declarative_base
from sqlalchemy_continuum import make_versioned

# Call this before defining your mapped classes.
make_versioned()

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    __versioned__ = {}

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)
