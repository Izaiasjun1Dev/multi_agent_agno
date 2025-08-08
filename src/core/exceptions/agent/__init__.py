"""
Exceções específicas para operações de Agent
Agent-specific exceptions
"""

from .agent_exceptions import (
    AgentAuthenticationException,
    AgentConnectionException,
    AgentCreationException,
    AgentDeletionException,
    AgentListException,
    AgentNotFoundException,
    AgentPermissionException,
    AgentStreamException,
    AgentUpdateException,
    AgentValidationException,
)

__all__ = [
    "AgentCreationException",
    "AgentNotFoundException",
    "AgentUpdateException",
    "AgentDeletionException",
    "AgentListException",
    "AgentValidationException",
    "AgentStreamException",
    "AgentAuthenticationException",
    "AgentPermissionException",
    "AgentConnectionException",
]
