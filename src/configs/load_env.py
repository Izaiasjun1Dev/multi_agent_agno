from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the application, loaded from environment variables.
    """
    app_prefix: str = Field(default="inner")
    environment: str = Field(default="development")
    aws_access_key_id: Optional[str] = Field(default=None)
    aws_secret_access_key: Optional[str] = Field(default=None)
    region_name: Optional[str] = Field(default=None)

load_dotenv()
settings = Settings()
