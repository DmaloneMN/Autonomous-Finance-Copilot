"""High-level service wrapper for Microsoft Foundry Agent Service."""
from __future__ import annotations

from src.services.foundry_client import build_project_client


class FoundryAgentService:
    def __init__(self) -> None:
        self.project_client = build_project_client()

    def get_agent_definition(self, name: str, instructions: str, tools: list[dict] | None = None) -> dict:
        return {
            "name": name,
            "model": "foundry-configured",
            "instructions": instructions,
            "tools": tools or [],
        }

    async def run_agent(self, *, name: str, instructions: str, user_input: str, context: dict) -> dict:
        del context
        return {
            "agent": name,
            "instructions": instructions,
            "response": f"Foundry placeholder response for: {user_input}",
        }
