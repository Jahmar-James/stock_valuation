from contextlib import contextmanager
from typing import Iterator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SessionLocal

class DatabaseManager:
    """Manages the database connection and provides sessions."""
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)

    @contextmanager
    def get_session(self) -> Iterator[SessionLocal]:
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
