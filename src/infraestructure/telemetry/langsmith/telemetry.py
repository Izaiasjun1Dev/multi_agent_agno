import logging
import os
from typing import Optional, Union

from agno.agent import Agent
from agno.team.team import Team

from configs.load_env import settings

logger = logging.getLogger(__name__)


class LangSmithTelemetry:
    """
    LangSmith telemetry integration for tracing agent operations.
    Configures LangSmith environment variables for automatic tracing.
    """

    def __init__(self, agent: Union[Agent, Team]) -> None:
        self.agent = agent
        self.is_enabled = False
        self._setup_telemetry()

    def _setup_telemetry(self) -> None:
        """Setup LangSmith telemetry configuration"""

        if not settings.langsmith_api_key:
            logger.warning("LangSmith API key not found. Telemetry disabled.")
            return

        if not settings.langsmith_tracing:
            logger.info("LangSmith tracing disabled in settings.")
            return

        try:
            # Configure LangSmith environment variables for automatic tracing
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
            os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project
            os.environ["LANGCHAIN_ENDPOINT"] = settings.langsmith_endpoint

            self.is_enabled = True

            logger.info(
                f"✅ LangSmith telemetry enabled for project '{settings.langsmith_project}'"
            )
            logger.info(f"📊 Traces will be sent to: {settings.langsmith_endpoint}")

        except Exception as e:
            logger.error(f"❌ Failed to setup LangSmith telemetry: {e}")
            self.is_enabled = False

    def get_status(self) -> dict:
        """Get telemetry status information"""
        return {
            "enabled": self.is_enabled,
            "project": settings.langsmith_project if self.is_enabled else None,
            "endpoint": settings.langsmith_endpoint if self.is_enabled else None,
            "api_key_configured": bool(settings.langsmith_api_key),
        }


# Global telemetry setup function
def setup_global_telemetry() -> bool:
    """
    Setup global LangSmith telemetry configuration.
    Call this once at application startup.
    """
    try:
        if settings.langsmith_api_key and settings.langsmith_tracing:
            # Configure environment variables globally
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
            os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project
            os.environ["LANGCHAIN_ENDPOINT"] = settings.langsmith_endpoint

            logger.info(
                f"🚀 Global LangSmith telemetry configured for project: {settings.langsmith_project}"
            )
            return True
        else:
            logger.info("LangSmith telemetry not configured globally.")
            return False
    except Exception as e:
        logger.error(f"Failed to setup global telemetry: {e}")
        return False
