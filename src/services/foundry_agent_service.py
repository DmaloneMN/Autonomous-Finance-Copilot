"""High-level service wrapper for Microsoft Foundry Agent Service."""
from __future__ import annotations

import json
import logging
from typing import Any

from src.core.exceptions import AgentError
from src.services.foundry_client import build_project_client

logger = logging.getLogger(__name__)


class FoundryAgentService:
    def __init__(self) -> None:
        self.project_client = build_project_client()

    def get_agent_definition(self, name: str, instructions: str, tools: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        return {
            "name": name,
            "model": "foundry-configured",
            "instructions": instructions,
            "tools": tools or [],
        }

    async def run_agent(
        self,
        *,
        name: str,
        instructions: str,
        user_input: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        payload = {
            "agent_name": name,
            "instructions": instructions,
            "user_input": user_input,
            "context": context,
        }

        try:
            response = await self._execute_agent(payload)
            return {
                "agent": name,
                "status": "completed",
                "request": payload,
                "response": response,
            }
        except Exception as exc:  # noqa: BLE001
            logger.exception("foundry_agent_run_failed", extra={"agent": name})
            raise AgentError(name, f"Foundry agent execution failed: {exc}") from exc

    async def _execute_agent(self, payload: dict[str, Any]) -> dict[str, Any]:
        del self.project_client
        response_text = self._build_response_text(payload)
        return {
            "message": response_text,
            "citations": [],
            "run_id": f"run-{payload['agent_name']}",
        }

    def _build_response_text(self, payload: dict[str, Any]) -> str:
        context_json = json.dumps(payload["context"], sort_keys=True)
        return (
            f"Simulated Foundry response for {payload['agent_name']} with query "
            f"'{payload['user_input']}' and context {context_json}."
        )
