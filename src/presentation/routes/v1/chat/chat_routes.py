from typing import Any, Dict

from fastapi import APIRouter, Body, Depends, Path, status

from presentation.controllers.chat.chat_controller import ChatController, AsyncChatController
from presentation.dependencies import get_bearer_token, get_async_chat_controller

router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
    responses={
        404: {"description": "Chat not found"},
        500: {"description": "Internal server error"},
    },
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new chat",
    description="Creates a new chat in the system",
    response_description="Chat created successfully",
    responses={
        201: {"description": "Chat created successfully"},
        400: {"description": "Invalid data"},
        409: {"description": "Chat already exists"},
    },
)
async def create_chat(
    controller: AsyncChatController = Depends(get_async_chat_controller),
    token: str = Depends(get_bearer_token),
) -> Dict[str, Any]:
    """
    Create a new chat in the system.

    - **chat_data**: Data for the new chat
    """
    result = await controller.create_chat(token)
    return result.model_dump()
