from abc import ABC, abstractmethod
from core.entities.user import User

class UserInterface(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        """
        Create a new user. 
        :param user: User object containing user details.
        :return: The created User object.
        """
        
        pass
    
    @abstractmethod
    def get_user(self, user_id: str) -> User:
        """
        Retrieve a user by their ID.
        :param user_id: The ID of the user to retrieve.
        :return: The User object if found, otherwise None.
        """
        
        pass
    
    @abstractmethod
    def update_user(self, user: User) -> User:
        """
        Update an existing user.
        :param user: User object containing updated user details.
        :return: The updated User object.
        """
        
        pass
    
    @abstractmethod
    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user by their ID.
        :param user_id: The ID of the user to delete.
        :return: True if the user was deleted successfully, otherwise False.
        """
        
        pass
    
    @abstractmethod
    def list_users(self) -> list[User]:
        """
        List all users.
        :return: A list of User objects.
        """
        
        pass
    
    
    