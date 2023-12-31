# Example architecture to work out data transfer between layers
# Desiging phase

# SETUP AND UTILITIES
from datetime import datetime
from typing import Type, Optional, Iterator, Tuple, List, Dict,Union
from contextlib import contextmanager
from pydantic import BaseModel as PydanticBaseModel, PrivateAttr, ConfigDict
from typing import Optional 
from sqlalchemy import create_engine, Column, Integer, String, select, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, Session, relationship, configure_mappers, mapped_column, Mapped, registry
from sqlalchemy_continuum import make_versioned

# Call this before defining your mapped classes.
make_versioned()

mapper_registry = registry()
Base = mapper_registry.generate_base()

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

class BaseORMVersioned(Base):
    """Base class for versioned tables."""
    __abstract__ = True
    __versioned__ = {}
    
    def __repr__(self):
        return f'ORM:<{self.__class__.__name__} {self.id}>'

# Soft delete mixin
class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True, default=None)

# ORM Model
class User(BaseORMVersioned):
    """User of the application, for multiple local users"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] =  mapped_column(String)
    age: Mapped[int] =  mapped_column(Integer)
    email: Mapped[str] =  mapped_column(String(100), unique=True)
    # A one-to-many relationship between User and UserPortfolio
    portfolios = relationship("UserPortfolio", back_populates="user", cascade="all, delete-orphan")
    
class UserPortfolio(BaseORMVersioned, SoftDeleteMixin):
    __tablename__ = 'portfolio'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # A many-to-one relationship between UserPortfolio and User
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    
# Other tables would be defined here
# Configuration, UserPortfolio, Holding, Stock, HistoricalMetric, Sector, HistoricalPrice, Dividend, Document, ValuationModel, Stock and Sector Association)

# Create tables
configure_mappers()

# DATA TRANSFER OBJECTS (DTOs) AND CONVERTERS

class BaseModelRepresentation(PydanticBaseModel):
    """Pydantic base model for data representation."""
    model_config = ConfigDict(from_attributes=True) # orm_mode is now from_attributes
    _processed_at: datetime = PrivateAttr(default_factory=datetime.utcnow)
    
    def __repr__(self):
        return f'DTO: <{self.__class__.__name__}>'


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

# DATA ACCESS (REPOSITORIES) CRUD OPERATIONS


# A utility to optionally provide a session or create a new one
@contextmanager
def provide_session(external_session=None) -> Iterator[Session]:
    if external_session:
        yield external_session
    else:
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

# CRUD Operations
class BaseRepository:
    """Base repository class to provide common CRUD operations from ORM objects (DAO)"""
    def __init__(self, model: Type[BaseORMVersioned]):
        self.model = model

    def create_entity(self, entity: BaseORMVersioned, current_session: Optional[Session] = None) -> Tuple[bool, int]:
        with provide_session(current_session) as active_session:
            try:
                active_session.add(entity)
                active_session.flush() 
                return True, entity.id
            except Exception as e:
                print(f"Error adding entity ({entity}): {e}")
                return False, -1

    def retrieve_entity_by_id(self, entity_id: int, session: Optional[Session] = None) -> Optional[BaseORMVersioned]:
        with provide_session(session) as active_session:
            entity = active_session.query(self.model).get(entity_id).first()
            if entity:
                active_session.expunge(entity)
                return entity
            else:
                return None
    
    def update_entity(self, entity: BaseORMVersioned, session: Optional[Session] = None) -> bool:
        with provide_session(session) as active_session:
            try:
                active_session.merge(entity)
                return True
            except Exception as e:
                print(f"Error updating entity: {e}")
                return False

    def delete_entity_by_id(self, entity_id: int, session: Optional[Session] = None) -> bool:
        with provide_session(session) as active_session:
            entity = self.retrieve_entity_by_id(entity_id, active_session)
            if not entity:
                print(f"Entity with ID {entity_id} does not exist. Cannot delete.")
                return False
            try:
                entity = self.retrieve_entity_by_id(entity_id, active_session)
                active_session.delete(entity)
                return True
            except Exception as e:
                print(f"Error deleting entity: {e}")
                return False

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=User)

    def create_user(self, user: User,session) -> Tuple[bool, int]:
        try:
            status, user_id = super().create_entity(user,session)
            return status, user_id
        except Exception as e:
            print(f"Error adding user: {e}")  
            return False, -1

    def retrieve_user_by_id(self, user_id: int,session) -> Optional[User]:
        return super().retrieve_entity_by_id(user_id, session)


class BaseConverter:
    """Converts between ORM and DTO objects"""
    def __init__(self, data:Union[UserDataTransfer, User],dto_class: Type[PydanticBaseModel], orm_class: Type[Base]):
        self.dto_class = dto_class
        self.orm_class = orm_class
        self.dto = None
        self.orm = None
        self.current_representation = None

        # To create a intance which pressive the data
        if isinstance(data, self.dto_class):
            self.current_representation = "DTO"
            self.dto = data
            self.orm = BaseConverter.convert_to_orm(data, self.orm_class)
        elif isinstance(data, self.orm_class):
            self.current_representation = "ORM"
            self.dto = BaseConverter.convert_to_transfer_model(data, self.dto_class)
            self.orm = data
    
    def toggle_model_form(self):
        if self.current_representation == "DTO":
            self.orm = BaseConverter.convert_to_orm(self.dto, self.orm_class)
            self.current_representation = "ORM"
        elif self.current_representation == "ORM":
            self.dto = BaseConverter.convert_to_transfer_model(self.orm, self.dto_class)
            self.current_representation = "DTO"
        else:
            raise Exception("Invalid Representation")
        
    @staticmethod
    def convert_to_orm(dto: PydanticBaseModel, model_class: Type[BaseORMVersioned]) -> BaseORMVersioned:
        return model_class(**dto.model_dump())

    @staticmethod
    def convert_to_transfer_model(orm_obj: BaseORMVersioned, dto_class: Type[PydanticBaseModel]) -> PydanticBaseModel:
        return dto_class.model_validate(orm_obj)

# If you need specific handling for User entities, then UserModelConverter makes sense. 
# Otherwise, just use the BaseConverter directly
class UserBaseConverter(BaseConverter):
    """ Converts between User ORM and UserDataTransfer DTO objects
        Allow for mapping attributes with different names or not contained in db
    """
    def __init__(self, data:Union[UserDataTransfer, User]):
        super().__init__(data, UserDataTransfer, User)
    # Your DTO fields here
  

 # SERVICE AND BUSINESS LOGIC LAYER

class DatabaseManager:
    """Manages the database connection and provides sessions."""
    def __init__(self, database_url: str):
        self.config = None # Config class wtih database_url
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.metadata = MetaData(self.engine)
        self._reflect_metadata()
        tables =  None # Temp 
        if tables:
            self._set_internal_databse_tables(tables)

    def _reflect_metadata(self) -> None:
        """Reflect the database metadata."""
        self.metadata.reflect(bind=self.engine)

    def _set_internal_databse_tables(self) -> None:
        """Set the internal database tables."""
        for table in self.metadata.tables:
            setattr(self, table, self.metadata.tables[table])

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

class DatabaseQueryExecutor:
    """Handles direct SQL queries and their results."""
    # only SELECT statements
    # Selected “Known” Functions These are GenericFunction class sqlalchemy.sql.functions.
    # array_agg Support for the ARRAY_AGG function.
    # min The SQL MIN() aggregate function.

    def __init__(self, db_manager: DatabaseManager):
        self._db_manager = db_manager

    def execute_select(self, select_statement: str) -> List[dict]:
        with self._db_manager.get_session() as session:
            result = session.execute(select_statement)
            return [dict(row) for row in result]
        
    def retrieve_all_entries(self, model: Type[BaseORMVersioned]) -> List[BaseORMVersioned]:
        with self._db_manager.get_session() as session:
            return session.query(model).all()
        
    def retrieve_entries_pagination(self, model: Type[BaseORMVersioned], page: int = 1, items_per_page: int = 10) -> List[BaseORMVersioned]:
        offset = (page - 1) * items_per_page
        with self._db_manager.get_session() as session:
            return session.query(model).offset(offset).limit(items_per_page).all()

    def retrieve_entry_by_id(self, model: Type[BaseORMVersioned], record_id: int) -> BaseORMVersioned:
        with self._db_manager.get_session() as session:
            return session.query(model).get(record_id)

    def retrieve_entries_by_conditions(self, model: Type[BaseORMVersioned], conditions: Dict) -> List[BaseORMVersioned]:
        with self._db_manager.get_session() as session:
            return session.query(model).filter_by(**conditions).all()

    def count_entries_with_conditions(self, model: Type[BaseORMVersioned], conditions: Dict = None) -> int:
        with self._db_manager.get_session() as session:
            query = session.query(model)
            if conditions:
                query = query.filter_by(**conditions)
            return query.count()

    def does_entry_exist(self, model: Type[BaseORMVersioned], conditions: Dict) -> bool:
        with self._db_manager.get_session() as session:
            return session.query(model).filter_by(**conditions).first() is not None

    def retrieve_model_columns(self, model: Type[BaseORMVersioned]) -> List[str]:
        with self._db_manager.get_session() as session:
            mapper = model.__mapper__
            return [column.key for column in mapper.columns]
        
    def joined_tables_by_id(self, model_1: Type[BaseORMVersioned], model_2: Type[BaseORMVersioned]) -> List[BaseORMVersioned]:
        statment = select(model_1).join(model_1.id == model_2.id)
        with self._db_manager.get_session() as session:
            return session.execute(statment).all()

class UserService:
    def __init__(self, user_repository: UserRepository, db_manager: DatabaseManager):
        self.user_repository = user_repository
        self.db_manager = db_manager

    def create_user(self, user_dto: UserDataTransfer) -> UserDataTransfer:
        with self.db_manager.get_session() as session:
            orm_user = BaseConverter.convert_to_orm(user_dto, User)
            status, user_id = self.user_repository.create_user(orm_user, session)

            if status is False:
                raise ValueError(f"Failed to create user {user_dto.name}")
            # Fetch the created user. This might seem redundant but ensures the auto-generated fields are populated.
            # And, correctly updates the DTO with the new ID.
            user = self.user_repository.retrieve_user_by_id(user_id, session)
            return BaseConverter.convert_to_transfer_model(user, UserDataTransfer)
    
    def get_user_by_id(self, user_id: int, session: Session) -> UserDataTransfer:
        user = self.user_repository.retrieve_user_by_id(user_id, session)
        return BaseConverter.convert_to_transfer_model(user, UserDataTransfer)


# OPERATION INTERFACE (FACADE)
class UserOperations:
    """Provides a simplified interface for User operations. (Facade Pattern))"""
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def register_user(self, user_dto: UserDataTransfer) -> UserDataTransfer:
        user_repository = UserRepository()
        user_service = UserService(user_repository, self.db_manager)
        return user_service.create_user(user_dto)

    def get_user_by_id(self, user_id: int) -> UserDataTransfer:
        user_repository = UserRepository()
        user_service = UserService(user_repository, self.db_manager)
        return user_service.get_user_by_id(user_id)

# Usage
db_manager = DatabaseManager(DATABASE_URL)

# Interface Usage
new_user_dto = UserDataTransfer(name="John Doe", email="john@example.com")
user_interface = UserOperations(db_manager)
created_user_dto = user_interface.register_user(new_user_dto)

fetched_dto = user_interface.get_user_by_id(created_user_dto.id)
print(fetched_dto)

# Query Executor Usage
query_executor = DatabaseQueryExecutor(db_manager)                     
# Get all users:
all_users = query_executor.retrieve_all_entries(User)
for user in all_users:
    print(user.name, user.email)

# execute a custom select statement:
query_results = query_executor.execute_select("SELECT * FROM users;")
print(query_results)

# Check if a user with a specific email exists:
email_to_check = "example@example.com"
does_exist = query_executor.does_entry_exist(User, {"email": email_to_check})
print(f"User with email {email_to_check} exists: {does_exist}")

# Get columns of the User table:
user_columns = query_executor.retrieve_model_columns(User)
print("Columns in the User table:", user_columns)