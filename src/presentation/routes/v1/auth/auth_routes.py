from fastapi import APIRouter, Body, Depends, status
from core.dtos.auth.auth_dtos import LoginDto
from presentation.controllers.auth.auth_controller import AuthController
from presentation.dependencies import get_auth_controller

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="User Login",
    response_description="The JWT token for the logged-in user",
    responses={
        200: {"description": "Login successful"},
        400: {"description": "Invalid credentials"},
        401: {"description": "Unauthorized"},
    },
)
def login(
    credentials: LoginDto = Body(..., description="User credentials for login"),
    auth_controller: AuthController = Depends(get_auth_controller),
):
    """
    User login
    """
    LoginDto.model_validate(credentials)

    return auth_controller.login(credentials.email, credentials.password)

@router.post(
    "/confirm-email",
    status_code=status.HTTP_200_OK,
    summary="Confirm Email",
    response_description="Confirmation status",
    responses={
        200: {"description": "Email confirmed successfully"},
        400: {"description": "Invalid confirmation token"},
    },
)
def confirm_email(
    email: str = Body(..., description="User email"),
    token: str = Body(..., description="Email confirmation token"),
    auth_controller: AuthController = Depends(get_auth_controller),
):
    """
    Confirm user email
    """
    return auth_controller.confirm_email(email, token)