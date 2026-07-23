"""Dependency injection helpers for FastAPI."""
from functools import lru_cache

from src.agents.orchestrator import OrchestratorAgent
from src.services.kernel_factory import build_kernel


@lru_cache
def get_orchestrator() -> OrchestratorAgent:
    kernel = build_kernel()
    return OrchestratorAgent(kernel=kernel)
