from typing import Any, Dict

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from core.dtos.user.user_dtos import CreateRequestUserDto, ReponseUserDto
from presentation.controllers.user.user_controller import UserController
from presentation.dependencies import get_user_controller

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={
        404: {"description": "Usuário não encontrado"},
        500: {"description": "Erro interno do servidor"},
    },
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Cria um novo usuário no sistema",
    response_description="Usuário criado com sucesso",
    response_model=ReponseUserDto,
    responses={
        201: {
            "description": "Usuário criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "email": "user@example.com",
                            "first_name": "João",
                            "last_name": "Silva",
                        },
                    }
                }
            },
        },
        400: {"description": "Dados inválidos"},
        409: {"description": "Usuário já existe"},
    },
)
async def create_user(
    user_data: CreateRequestUserDto,
    controller: UserController = Depends(get_user_controller),
) -> Dict[str, Any]:
    """
    Criar um novo usuário no sistema.

    - **user_data**: Dados do usuário a ser criado
    """
    result = await controller.create_user(user_data)

    if not result.get("success", False):
        raise HTTPException(
            status_code=result.get(
                "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail=result.get("error", "Erro interno do servidor"),
        )

    return result


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    response_description="Dados do usuário",
)
async def get_user(
    user_id: str = Path(..., description="ID do usuário"),
    controller: UserController = Depends(get_user_controller),
) -> Dict[str, Any]:
    """
    Obter um usuário pelo ID.

    - **user_id**: ID do usuário
    """
    result = await controller.get_user(user_id)

    if not result.get("success", False):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_404_NOT_FOUND),
            detail=result.get("error", "Usuário não encontrado"),
        )

    return result


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="List all users",
    response_description="Lista de usuários",
)
async def list_users(
    controller: UserController = Depends(get_user_controller),
) -> Dict[str, Any]:
    """
    Listar todos os usuários.
    """
    result = await controller.list_users()

    if not result.get("success", False):
        raise HTTPException(
            status_code=result.get(
                "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail=result.get("error", "Erro interno do servidor"),
        )

    return result


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Update user",
    response_description="Usuário atualizado",
)
async def update_user(
    user_id: str = Path(..., description="ID do usuário"),
    user_data: CreateRequestUserDto = Body(..., description="Novos dados do usuário"),
    controller: UserController = Depends(get_user_controller),
) -> Dict[str, Any]:
    """
    Atualizar um usuário existente.

    - **user_id**: ID do usuário
    - **user_data**: Novos dados do usuário
    """
    result = await controller.update_user(user_id, user_data)

    if not result.get("success", False):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_404_NOT_FOUND),
            detail=result.get("error", "Usuário não encontrado"),
        )

    return result
