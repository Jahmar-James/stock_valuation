
class DBInitializer:
    def __init__(self, engine):
        self.engine = engine

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)
        print("Tables created successfully!")

    def initialize(self):
        # Add any other initialization steps you might have.
        self.create_tables()

class DatabaseManager:
    """Manages the database connection and provides sessions."""
    def __init__(self, config: Config, initializer: Optional[DBInitializer] = None):
        self.config = config
        self.engine = create_engine(self.config.DB_TEST)
        if not self._database_initialized():
            initializer = initializer or DBInitializer(self.engine)
            initializer.initialize()
        self.metadata = MetaData(bind =self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self._reflect_metadata()
        
    def _reflect_metadata(self) -> None:
        """Reflect the database metadata."""
        self.metadata.reflect(bind=self.engine)

    def _database_initialized(self) -> bool:
        # Implement logic to check if database (or specific tables) exists.
        pass
    
            
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

