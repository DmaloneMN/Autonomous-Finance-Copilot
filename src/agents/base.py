"""Base class for finance agents backed by Foundry Agent Service."""
from __future__ import annotations

from abc import ABC, abstractmethod

from src.agents.contracts import AgentContext, AgentResult
from src.services.foundry_agent_service import FoundryAgentService


class BaseAgent(ABC):
    agent_name: str = "base-agent"

    def __init__(self, foundry_service: FoundryAgentService) -> None:
        self.foundry_service = foundry_service

    @abstractmethod
    async def run(self, context: AgentContext) -> AgentResult:
        """Execute the agent against a shared context."""
