# app/dao/models/base.py
from sqlalchemy.orm import declarative_base
from sqlalchemy_continuum import make_versioned, versioning_manager,Versioned

# Call this before defining your mapped classes.
make_versioned()

Base = declarative_base()

class BaseModel(Base,Versioned):
    __abstract__ = True

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)
