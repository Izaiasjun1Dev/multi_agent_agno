from pydantic import BaseModel, Field

    
class CreateChatResponseDto(BaseModel):
    chat_id: str = Field(default="", title="Chat ID", description="Identifier of the created chat")
    message: str = Field(default="", title="Message", description="Confirmation message for chat creation")
    
    
