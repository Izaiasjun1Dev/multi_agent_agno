from typing import Any, Dict

from fastapi import APIRouter, Body, Depends, Path, status

from core.dtos.user.user_dtos import CreateRequestUserDto
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
    responses={
        201: {"description": "Usuário criado com sucesso"},
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
    return result


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    description="Obtém um usuário específico pelo ID",
    response_description="Usuário encontrado",
    responses={
        200: {"description": "Usuário encontrado"},
        404: {"description": "Usuário não encontrado"},
    },
)
async def get_user(
    user_id: str = Path(..., description="ID do usuário"),
    controller: UserController = Depends(get_user_controller),
) -> Dict[str, Any]:
    """
    Obter informações de um usuário específico.

    - **user_id**: ID único do usuário
    """
    return await controller.get_user(user_id)


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Update user",
    description="Atualiza os dados de um usuário existente",
    response_description="Usuário atualizado",
    responses={
        200: {
            "description": "Usuário atualizado com sucesso",
        },
        404: {"description": "Usuário não encontrado"},
        400: {"description": "Dados inválidos"},
    },
)
async def update_user(
    user_id: str = Path(..., description="ID do usuário"),
    user_data: CreateRequestUserDto = Body(..., description="Novos dados do usuário"),
    controller: UserController = Depends(get_user_controller),
) -> Dict[str, Any]:
    """
    Atualizar os dados de um usuário existente.

    - **user_id**: ID único do usuário
    - **user_data**: Novos dados do usuário
    """
    return await controller.update_user(user_id, user_data)
