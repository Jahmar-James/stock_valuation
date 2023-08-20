# app/dao/repository/user_repository.py
from typing import Optional, Tuple
from app.dao.repository.base_repository import BaseRepository
from sqlalchemy.orm import Session
from app.dao.models.user import User

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=User)

    def create_user(self, user: User, session: Optional[Session] = None) -> Tuple[bool, int]:
            """
            Create a new user in the database.

            :param user: The user object to be added.
            :param session: Optional SQLAlchemy session. If not provided, a new session is created.
            :return: Tuple with a boolean indicating success or failure and the user's ID or -1 if failed.
            """
            try:
                status, user_id = super().create_entity(user, session)
                return status, user_id
            except Exception as e:
                print(f"Error adding user: {e} | DAO Layer")  
                return False, -1

    def retrieve_user_by_id(self, user_id: int, session: Optional[Session] = None) -> Optional[User]:
        """
        Retrieve a user from the database based on their ID.

        :return: User object or None if not found.
        """
        return super().retrieve_entity_by_id(user_id, session)

    def retrieve_user_by_username(self, username: str, session: Optional[Session] = None) -> Optional[User]:
        """
        Retrieve a user from the database based on their username.
        :return: User object or None if not found.
        """
        return super().retrieve_entity_by_attribute(User.username, username, session)

    def retrieve_all_users(self, session: Optional[Session] = None) -> Optional[User]:
        """
        Retrieve all users from the database.

        :return: List of User objects or None if not found.
        """
        return super().retrieve_all_entities(session)

    def update_user(self, user: User, session: Optional[Session] = None) -> bool:
        """
        Update a user in the database.

        :return: Boolean indicating success or failure.
        """
        try:
            super().update_entity(user, session)
            return True
        except Exception as e:
            print(f"Error updating user: {e} | DAO Layer")
            return False

    def delete_user_by_id(self, user_id: int, session: Optional[Session] = None) -> bool:
        """
        Delete a user from the database.
        :return: Boolean indicating success or failure.
        """
        try:
            super().delete_entity(user_id, session)
            return True
        except Exception as e:
            print(f"Error deleting user: {e} | DAO Layer")
    
"""
Note for future implementations:

1. **Error Handling**:
   - Logs: Be as descriptive as necessary. Include components/layers for clarity (e.g., "DAO Layer").
   - User-facing Messages: Keep these generic to avoid security risks. Do not expose technical details or internal mechanics. 
     Example: Instead of "Failed to connect to database", use "An internal error occurred. Please try again later."

2. **Logging**:
   - implementing a logging system for better traceability and debugging after the applcation is ready for testing.
   - If an error occurs, consider giving a unique ID to each error and displaying this ID to the user. This will allow for easier tracking without exposing technical details.

3. **Security**:
   - Sanitize any error messages that may be sent to the front end. Avoid revealing specifics about the database or internal processes.
   - Always be cautious about revealing the inner workings of the application to end-users.
"""
