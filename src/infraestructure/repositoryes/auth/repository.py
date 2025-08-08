from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from configs.load_env import settings
from core.dtos.auth.auth_dtos import UserDetailsResponseDto
from core.exceptions.auth.auth_exceptions import (
    AuthenticationException,
    InvalidCredentialsException,
)
from infraestructure.client_factory.aws import AWSClientFactory
from interface.auth.auth_interface import AuthInterface


class AuthRepository(AuthInterface):
    def __init__(self):
        self.aws = AWSClientFactory()
        self.cognito = self.aws.cognito()
        self.user_pool_id = settings.cognito_user_pool_id
        self.user_pool_client_id = settings.cognito_user_pool_client_id

    def signup(
        self,
        email: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Sign up a new user and return their details.
        """
        try:
            # Preparar atributos do usuário usando apenas atributos padrão do Cognito
            user_attributes = [
                {"Name": "email", "Value": email},
                {
                    "Name": "name",
                    "Value": f"{first_name or ''} {last_name or ''}".strip(),
                },
            ]

            resp = self.cognito.sign_up(
                ClientId=self.user_pool_client_id,
                Username=email,
                Password=password,
                ValidationData=user_attributes,
                UserAttributes=user_attributes,
            )
            return {"user_sub": resp["UserSub"], "email": email}
        except Exception as e:
            return {"error": str(e)}

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate a user and return authentication details.
        """
        try:
            resp = self.cognito.initiate_auth(
                ClientId=self.user_pool_client_id,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": email,
                    "PASSWORD": password,
                },
            )
            return {
                "access_token": resp["AuthenticationResult"]["AccessToken"],
                "refresh_token": resp["AuthenticationResult"].get("RefreshToken"),
                "id_token": resp["AuthenticationResult"].get("IdToken"),
                "token_type": resp["AuthenticationResult"]["TokenType"],
                "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
            }

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            if error_code == "NotAuthorizedException":
                raise InvalidCredentialsException(details={"email": email})
            raise AuthenticationException(
                message_pt="Falha na autenticação",
                message_en="Authentication failed",
                details={"email": email, "error": str(e)},
            )

        except Exception as e:
            return {"error": str(e)}

    def logout(self, token: str) -> bool:
        """
        Log out a user by invalidating their token.
        """
        try:
            self.cognito.global_sign_out(AccessToken=token)
            return True
        except Exception as e:
            return False

    def reset_password(self, email: str, new_password: str) -> bool:
        """
        Reset the password for a user.
        """
        try:
            resp = self.cognito.admin_set_user_password(
                UserPoolId=self.user_pool_id,
                Username=email,
                Password=new_password,
                Permanent=True,
            )
            return True
        except Exception as e:
            return False

    def get_user_details(self, token: str) -> Optional[UserDetailsResponseDto]:
        """
        Retrieve details of the authenticated user using their token.
        """
        try:
            resp = self.cognito.get_user(AccessToken=token)
            user_attributes = {
                attr["Name"]: attr["Value"] for attr in resp["UserAttributes"]
            }
            full_name = user_attributes.get("name", "")
            first_name = full_name.split()[0] if full_name else ""
            last_name = (
                " ".join(full_name.split()[1:]) if len(full_name.split()) > 1 else ""
            )

            return UserDetailsResponseDto(
                user_id=user_attributes.get("sub", ""),
                user_sub=user_attributes.get("sub", ""),
                email=user_attributes.get("email", ""),
                first_name=first_name,
                last_name=last_name,
                name=full_name,
                email_verified=user_attributes.get("email_verified", "true").lower()
                == "true",
                is_active=True,  # Cognito doesn't provide active status directly
            )
        except Exception as e:
            return None

    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh an access token using a refresh token.
        """
        try:
            resp = self.cognito.initiate_auth(
                ClientId=self.user_pool_client_id,
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={
                    "REFRESH_TOKEN": refresh_token,
                },
            )
            return {
                "access_token": resp["AuthenticationResult"]["AccessToken"],
                "token_type": resp["AuthenticationResult"]["TokenType"],
                "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
            }
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            return {"error": f"Failed to refresh token: {error_code}"}
        except Exception as e:
            return {"error": str(e)}

    def resend_confirmation_code(self, email: str) -> bool:
        """
        Resend confirmation code to user's email.
        """
        try:
            self.cognito.resend_confirmation_code(
                ClientId=self.user_pool_client_id,
                Username=email,
            )
            return True
        except ClientError as e:
            return False
        except Exception as e:
            return False

    def list_active_sessions(self) -> List[Dict[str, Any]]:
        """
        List all active sessions for users.
        Note: AWS Cognito doesn't provide a direct API to list all active sessions.
        This would require custom implementation using DynamoDB or other session tracking.
        """
        # TODO: Implement session tracking mechanism
        return []

    def revoke_session(self, token: str) -> bool:
        """
        Revoke an active session using the user's token.
        """
        try:
            # AWS Cognito uses global_sign_out for revoking tokens
            self.cognito.global_sign_out(AccessToken=token)
            return True
        except Exception as e:
            return False

    def confirm_email(self, email: str, token: str) -> bool:
        """
        Confirm a user's email address using a confirmation token.
        Note: In Cognito, this is typically done with username and confirmation code.
        The token parameter here could be a composite of username:code.
        """
        try:
            self.cognito.confirm_sign_up(
                ClientId=self.user_pool_client_id,
                Username=email,
                ConfirmationCode=token,
            )
            return True
        except ClientError as e:
            return False
        except Exception as e:
            return False
