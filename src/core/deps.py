"""Dependency injection helpers for FastAPI."""
from functools import lru_cache

from src.agents.orchestrator import OrchestratorAgent
from src.services.foundry_agent_service import FoundryAgentService


@lru_cache
def get_foundry_service() -> FoundryAgentService:
    return FoundryAgentService()


@lru_cache
def get_orchestrator() -> OrchestratorAgent:
    return OrchestratorAgent(foundry_service=get_foundry_service())
