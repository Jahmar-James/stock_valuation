# Example architecture to work out data transfer between layers
# Desiging phase

# SETUP AND UTILITIES
 
from typing import Type, Optional, Iterator, Tuple, List, Dict
from contextlib import contextmanager
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
from sqlalchemy_continuum import make_versioned, versioning_manager,Versioned

# Call this before defining your mapped classes.
make_versioned()

Base = declarative_base()

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)



# ORM Model
class User(Base, Versioned):
    """ORM representation of the User Table conteain user entitres"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

# Other tables would be defined here
# Configuration, UserPortfolio, Holding, Stock, HistoricalMetric, Sector, HistoricalPrice, Dividend, Document, ValuationModel, Stock and Sector Association)

# Create tables
versioning_manager.init(Base)
Base.metadata.create_all(bind=engine)

# DATA TRANSFER OBJECTS (DTOs) AND CONVERTERS

class UserDataTransfer(BaseModel):
    """ Model for transferring User data. (DTO))"""
    id: Optional[int]
    name: str
    email: str

    model_config = {"from_attributes": True}

# DATA ACCESS (REPOSITORIES) CRUD OPERATIONS


# A utility to optionally provide a session or create a new one
@contextmanager
def provide_session(external_session=None) -> Iterator[SessionLocal]:
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
    def __init__(self, model: Type[Base]):
        self.model = model

    def create_entity(self, entity: Base, session: Optional[SessionLocal] = None) -> Tuple[bool, int]:
        with provide_session(session) as s:
            try:
                s.add(entity)
                s.flush()  # Get the ID without committing if it's an external session
                return True, entity.id
            except Exception as e:
                # Handle specific exceptions and logging as needed
                print(f"Error adding entity ({entity}): {e}")
                return False, -1

    def retrieve_entity_by_id(self, entity_id: int, session: Optional[SessionLocal] = None) -> Optional[Base]:
        with provide_session(session) as s:
            return s.query(self.model).filter_by(id=entity_id).first()
    
    def update_entity(self, entity: Base, session: Optional[SessionLocal] = None) -> bool:
        with provide_session(session) as s:
            try:
                s.merge(entity)
                return True
            except Exception as e:
                print(f"Error updating entity: {e}")
                return False

    def delete_entity_by_id(self, entity_id: int, session: Optional[SessionLocal] = None) -> bool:
        with provide_session(session) as s:
            try:
                entity = self.retrieve_entity_by_id(entity_id, s)
                s.delete(entity)
                return True
            except Exception as e:
                print(f"Error deleting entity: {e}")
                return False

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=User)

    def create_user(self, user: User) -> Tuple[bool, int]:
        try:
            status, user_id = super().create_entity(user)
            return status, user_id
        except Exception as e:
            print(f"Error adding user: {e}")  
            return False, -1

    def retrieve_user_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(User).filter_by(id=user_id).first()


class ModelConverterBase:
    """Converts between ORM and DTO objects"""
    def __init__(self, data:[UserDataTransfer, User]):
        # To create a intance which pressive the data
        if isinstance(data, UserDataTransfer):
            self.current_representation = "DTO"
            self.dto = data
            self.orm = ModelConverterBase.to_orm(data, User)
        elif isinstance(data, User):
            self.current_representation = "ORM"
            self.dto = ModelConverterBase.to_dto(data, UserDataTransfer)
            self.orm = data
    
    def toggle_model_form(self):
        if self.current_representation == "DTO":
            self.orm = ModelConverterBase.to_orm(self.dto, User)
            self.current_representation = "ORM"
        elif self.current_representation == "ORM":
            self.dto = ModelConverterBase.to_dto(self.orm, UserDataTransfer)
            self.current_representation = "DTO"
        else:
            raise Exception("Invalid Representation")
        
    @staticmethod
    def convert_to_orm(dto: BaseModel, model_class: Type[Base]) -> Base:
        return model_class(**dto.model_dump())

    @staticmethod
    def convert_to_transfer_model(orm_obj: Base, dto_class: Type[BaseModel]) -> BaseModel:
        return dto_class.model_validate(orm_obj)

# If you need specific handling for User entities, then UserModelConverter makes sense. 
# Otherwise, just use the ModelConverterBase directly
class UserModelConverter(ModelConverterBase):
    """Allow for mapping attributes with different names or not contained in db"""
    # Your DTO fields here

 # SERVICE AND BUSINESS LOGIC LAYER

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

class DatabaseQueryExecutor:
    """Handles direct SQL queries and their results."""
    # only SELECT statements
    def __init__(self, db_manager: DatabaseManager):
        self._db_manager = db_manager

    def execute_select(self, select_statement: str) -> List[dict]:
        with self._db_manager.get_session() as session:
            result = session.execute(select_statement)
            return [dict(row) for row in result]
        
    def retrieve_all_entries(self, model: Type[Base]) -> List[Base]:
        with self._db_manager.get_session() as session:
            return session.query(model).all()
        
    def retrieve_all_entries_pagination(self, model: Type[Base], page: int = 1, items_per_page: int = 10) -> List[Base]:
        offset = (page - 1) * items_per_page
        with self._db_manager.get_session() as session:
            return session.query(model).offset(offset).limit(items_per_page).all()

    def retrieve_entry_by_id(self, model: Type[Base], record_id: int) -> Base:
        with self._db_manager.get_session() as session:
            return session.query(model).get(record_id)

    def retrieve_entries_by_conditions(self, model: Type[Base], conditions: Dict) -> List[Base]:
        with self._db_manager.get_session() as session:
            return session.query(model).filter_by(**conditions).all()

    def count_entries_with_conditions(self, model: Type[Base], conditions: Dict = None) -> int:
        with self._db_manager.get_session() as session:
            query = session.query(model)
            if conditions:
                query = query.filter_by(**conditions)
            return query.count()

    def does_entry_exist(self, model: Type[Base], conditions: Dict) -> bool:
        with self._db_manager.get_session() as session:
            return session.query(model).filter_by(**conditions).first() is not None

    def retrieve_model_columns(self, model: Type[Base]) -> List[str]:
        with self._db_manager.get_session() as session:
            mapper = model.__mapper__
            return [column.key for column in mapper.columns]
        
    def joined_tables_by_id(self, model_1: Type[Base], model_2: Type[Base]) -> List[Base]:
        statment = select(model_1).join(model_1.id == model_2.id)
        with self._db_manager.get_session() as session:
            return session.execute(statment).all()

class UserService:
    def __init__(self, user_repository: UserRepository, db_manager: DatabaseManager):
        self.user_repository = user_repository
        self.db_manager = db_manager

    def create_user(self, user_dto: UserDataTransfer) -> UserDataTransfer:
        with self.db_manager.get_session() as session:
            orm_user = ModelConverterBase.convert_to_orm(user_dto, User)
            status, user_id = self.user_repository.create_user(orm_user, session)

            if status is False:
                raise ValueError(f"Failed to create user {user_dto.name}")
            # Fetch the created user. This might seem redundant but ensures the auto-generated fields are populated.
            # And, correctly updates the DTO with the new ID.
            user = self.user_repository.retrieve_user_by_id(user_id, session)
            return ModelConverterBase.convert_to_transfer_model(user, UserDataTransfer)
    
    def get_user_by_id(self, user_id: int, session: SessionLocal) -> UserDataTransfer:
        user = self.user_repository.retrieve_user_by_id(user_id, session)
        return ModelConverterBase.convert_to_transfer_model(user, UserDataTransfer)


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