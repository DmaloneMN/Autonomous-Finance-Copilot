"""Orchestrator agent endpoint."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from src.agents.orchestrator import OrchestratorAgent
from src.core.deps import get_orchestrator

router = APIRouter()


class AnalysisRequest(BaseModel):
    query: str = Field(..., description="Natural language finance question")
    fiscal_period: str = Field(..., description="Fiscal period such as 2026-Q1")
    context: dict = Field(default_factory=dict, description="Optional finance context payload")


class AnalysisResponse(BaseModel):
    trace_id: str
    fiscal_period: str
    summary: str
    agent_outputs: dict
    evaluation: dict


@router.post("/run", response_model=AnalysisResponse)
async def run_analysis(
    request: AnalysisRequest,
    orchestrator: OrchestratorAgent = Depends(get_orchestrator),
) -> AnalysisResponse:
    result = await orchestrator.run(request.query, request.fiscal_period, request.context)
    return AnalysisResponse(**result)
