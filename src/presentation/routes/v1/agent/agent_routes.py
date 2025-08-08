from typing import Any, Dict

from fastapi import APIRouter, Body, Depends, Path, status
from fastapi.responses import StreamingResponse

from core.dtos.agent.agent_dtos import CreateAgentDTO, StreamChatRequestDTO
from presentation.controllers.agent.agent_controller import AgentController
from presentation.dependencies import get_agent_controller, get_bearer_token

router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
    responses={
        404: {"description": "Agent not found"},
        500: {"description": "Internal server error"},
    },
)


@router.post(
    "/stream-chat",
    status_code=status.HTTP_200_OK,
    summary="Stream chat messages",
    description="Stream chat messages for an agent",
    response_description="Streaming chat response",
    responses={
        200: {"description": "Streaming response started successfully"},
        400: {"description": "Invalid data"},
        401: {"description": "Invalid token"},
        500: {"description": "Internal server error"},
    },
)
async def stream_chat(
    request_data: StreamChatRequestDTO,
    controller: AgentController = Depends(get_agent_controller),
    token: str = Depends(get_bearer_token),
) -> StreamingResponse:
    """
    Stream chat messages for a specific agent.

    - **request_data**: Object containing the list of messages to process and stream response
    """

    # Converter DTO para formato esperado pelo controller
    messages = []
    for msg in request_data.messages:
        message_dict = {
            "role": msg.role,
            "content": msg.content,
        }

        # Adicionar metadata se não estiver vazio
        if msg.metadata:
            message_dict.update(msg.metadata)

        messages.append(message_dict)

    response = controller.stream_chat_response(token, messages)

    return StreamingResponse(response, media_type="text/event-stream")
