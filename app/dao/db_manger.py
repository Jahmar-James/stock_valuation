from typing import Optional, Type, Iterator
from contextlib import contextmanager
from sqlalchemy.orm import Session, sessionmaker, configure_mappers, registry
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import NoSuchTableError
from app.dao.models import User

from config import Config

class DBInitializer:
    def __init__(self, engine: registry,session: Type[Session]):
        self.engine = engine
        self.SessionLocal = session

    def create_tables(self):
        """Create all tables in the engine. This is equivalent to "Create Table"""
        from app.dao.models.base import Base
        from app.dao.models import ALL_MODELS
        configure_mappers()

        choice = input("Do you want to create tables? (yes/no): ").strip().lower()
        if choice == 'yes':
            Base.metadata.create_all(bind=self.engine)
            print("Tables created successfully!")
            print("Versioning manager initialized successfully!")
        else:
            print("Operation aborted.")
            
    def get_session(self):
        return self.SessionLocal()
    
    def initialize(self):
        self.create_tables()
        
class DatabaseManager:
    """Manages the database connection and provides sessions."""
    def __init__(self, config: Config, initializer: Optional[DBInitializer] = None):
        self.config = config
        self.engine = create_engine(self.config.DB_TEST)
        self.SessionLocal = sessionmaker(bind=self.engine)

        if not self._database_initialized():
            initializer = initializer or DBInitializer(self.engine, self.SessionLocal)
            initializer.initialize()
        
        self.metadata = MetaData(bind =self.engine)    
        
    def _database_initialized(self) -> bool:
        try:
            User.__table__.drop(self.engine, checkfirst=True)
            return True
        except NoSuchTableError:
            return False
            
    @contextmanager
    def get_session(self) -> Iterator[Session]:
        """Provide a session for database interactions."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()



if __name__ == "__main__":
    db_manager = DatabaseManager(Config)
