from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class AuthInterface(ABC):
    @abstractmethod
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Authenticate a user and return authentication details.
        :param username: The username of the user.
        :param password: The password of the user.
        :return: A dictionary containing authentication details such as token.
        """

        pass

    @abstractmethod
    def logout(self, token: str) -> bool:
        """
        Log out a user by invalidating their token.
        :param token: The authentication token of the user.
        :return: True if logout was successful, otherwise False.
        """

        pass

    @abstractmethod
    def signup(
        self,
        username: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Sign up a new user and return their details.
        :param username: The desired username for the new user.
        :param password: The desired password for the new user.
        :param first_name: The first name of the user (optional).
        :param last_name: The last name of the user (optional).
        :return: A dictionary containing the new user's details.
        """

        pass

    @abstractmethod
    def reset_password(self, username: str, new_password: str) -> bool:
        """
        Reset the password for a user.
        :param username: The username of the user whose password is to be reset.
        :param new_password: The new password for the user.
        :return: True if the password was reset successfully, otherwise False.
        """

        pass

    @abstractmethod
    def get_user_details(self, token: str) -> Dict[str, Any]:
        """
        Retrieve details of the authenticated user using their token.
        :param token: The authentication token of the user.
        :return: A dictionary containing user details if authenticated, otherwise None.
        """

        pass

    @abstractmethod
    def list_active_sessions(self) -> List[Dict[str, Any]]:
        """
        List all active sessions for users.
        :return: A list of dictionaries containing session details for each active session.
        """

        pass

    @abstractmethod
    def revoke_session(self, token: str) -> bool:
        """
        Revoke an active session using the user's token.
        :param token: The authentication token of the user.
        :return: True if the session was revoked successfully, otherwise False.
        """

        pass

    @abstractmethod
    def confirm_email(self, email: str, token: str) -> bool:
        """
        Confirm a user's email address using a confirmation token.
        :param email: The email address of the user.
        :param token: The confirmation token sent to the user's email.
        :return: True if the email was confirmed successfully, otherwise False.
        """

        pass
