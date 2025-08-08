from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the application, loaded from environment variables.
    """

    app_prefix: str = Field(default="inner")
    environment: str = Field(default="dev")
    aws_access_key_id: Optional[str] = Field(default=None)
    aws_secret_access_key: Optional[str] = Field(default=None)
    region_name: Optional[str] = Field(default=None)

    cognito_user_pool_id: Optional[str] = Field(default=None)
    cognito_user_pool_client_id: Optional[str] = Field(default=None)
    user_password: Optional[str] = Field(default=None)

    # PostgreSQL Configuration
    db_host: str = Field(default="localhost")
    db_port: str = Field(default="5432")
    db_user: str = Field(default="inner")
    db_password: str = Field(default="inner")
    db_name: str = Field(default="inner_chat")

    # agent configuration
    default_model: str = Field(
        default="gpt-4o-mini",
        title="Default Model",
        description="The default model to be used by the agent",
    )
    default_anthropic_model: str = Field(
        default="claude-sonnet-4-20250514",
    )
    openai_api_key: str = Field(
        default="",
        title="OpenAI API Key",
        description="API key for OpenAI services",
    )
    anthropic_api_key: str = Field(
        default="",
        title="Anthropic API Key",
        description="API key for Anthropic services",
    )
    debug_agent: bool = Field(
        default=True,
        title="Debug Agent",
        description="Enable debugging for the agent",
    )
    # langsmith configuration
    langsmith_api_key: str = Field(
        default="",
        title="LangSmith API Key",
        description="API key for LangSmith services",
    )
    langsmith_tracing: bool = Field(
        default=False,
        title="LangSmith Tracing",
        description="Enable tracing for LangSmith",
    )
    langsmith_endpoint: str = Field(
        default="https://api.smith.langchain.com",
        title="LangSmith Endpoint",
        description="Endpoint for LangSmith services",
    )
    langsmith_project: str = Field(
        default="default_project",
        title="LangSmith Project",
        description="Project name for LangSmith services",
    )


load_dotenv()
settings = Settings()
