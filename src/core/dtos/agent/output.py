from pydantic import BaseModel, Field
from typing import Optional, Literal

class AgentIntentOutputDto(BaseModel):
    intent: Literal[
        "generate_image",
        "route_llm",
        "default"
    ] = Field(..., description="Intent detected by the agent base on the user's history messages")
    metadata: Optional[dict] = Field(None, description="Additional metadata related to the intent")