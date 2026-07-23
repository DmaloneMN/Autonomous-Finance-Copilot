"""Domain exceptions and FastAPI exception handlers."""
from fastapi import Request
from fastapi.responses import JSONResponse


class AgentError(Exception):
    def __init__(self, agent: str, message: str) -> None:
        self.agent = agent
        self.message = message
        super().__init__(f"[{agent}] {message}")


class FabricConnectionError(Exception):
    """Raised when Microsoft Fabric or lakehouse access fails."""


class SearchIndexError(Exception):
    """Raised when Azure AI Search queries or index operations fail."""


async def agent_error_handler(request: Request, exc: AgentError) -> JSONResponse:
    del request
    return JSONResponse(
        status_code=500,
        content={"error": "agent_error", "agent": exc.agent, "detail": exc.message},
    )


async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    del request
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "detail": str(exc)},
    )
