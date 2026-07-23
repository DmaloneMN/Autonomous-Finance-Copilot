"""Orchestrator Agent coordinating all specialist agents."""
from __future__ import annotations

import uuid
from collections.abc import Iterable

from src.agents.anomaly_detection import AnomalyDetectionAgent
from src.agents.base import BaseAgent
from src.agents.budget import BudgetAgent
from src.agents.contracts import AgentContext, AgentResult
from src.agents.executive_summary import ExecutiveSummaryAgent
from src.agents.forecast import ForecastAgent
from src.agents.instructions import ORCHESTRATOR_INSTRUCTIONS
from src.agents.vendor_analysis import VendorAnalysisAgent
from src.agents.variance_analysis import VarianceAnalysisAgent
from src.evaluation.scorer import EvaluationScorer
from src.services.foundry_agent_service import FoundryAgentService


class OrchestratorAgent(BaseAgent):
    agent_name = "orchestrator-agent"

    def __init__(self, foundry_service: FoundryAgentService) -> None:
        super().__init__(foundry_service)
        self.variance_agent = VarianceAnalysisAgent(foundry_service)
        self.budget_agent = BudgetAgent(foundry_service)
        self.forecast_agent = ForecastAgent(foundry_service)
        self.vendor_agent = VendorAnalysisAgent(foundry_service)
        self.anomaly_agent = AnomalyDetectionAgent(foundry_service)
        self.executive_agent = ExecutiveSummaryAgent(foundry_service)
        self.scorer = EvaluationScorer()

    async def run(self, query: str, fiscal_period: str, inputs: dict) -> dict:
        trace_id = str(uuid.uuid4())
        context = AgentContext(
            fiscal_period=fiscal_period,
            query=query,
            trace_id=trace_id,
            inputs=inputs,
        )
        orchestrator_response = await self.foundry_service.run_agent(
            name=self.agent_name,
            instructions=ORCHESTRATOR_INSTRUCTIONS,
            user_input=query,
            context={"fiscal_period": fiscal_period, **inputs},
        )
        results = await self._run_specialists(context)
        executive_result = await self.executive_agent.run(context)
        all_results = [*results, executive_result]
        evaluation = self.scorer.score(all_results)
        return {
            "trace_id": trace_id,
            "fiscal_period": fiscal_period,
            "summary": executive_result.summary,
            "agent_outputs": {
                "orchestrator": orchestrator_response,
                **{result.agent_name: self._serialize_result(result) for result in all_results},
            },
            "evaluation": evaluation,
        }

    async def _run_specialists(self, context: AgentContext) -> list[AgentResult]:
        agents: Iterable[BaseAgent] = [
            self.variance_agent,
            self.budget_agent,
            self.forecast_agent,
            self.vendor_agent,
            self.anomaly_agent,
        ]
        results: list[AgentResult] = []
        for agent in agents:
            results.append(await agent.run(context))
        return results

    async def run_agent(self, context: AgentContext) -> AgentResult:
        result = await self.run(context.query, context.fiscal_period, context.inputs)
        return AgentResult(
            agent_name=self.agent_name,
            summary=result["summary"],
            metrics=result["evaluation"],
            artifacts=result["agent_outputs"],
        )

    def _serialize_result(self, result: AgentResult) -> dict:
        return {
            "summary": result.summary,
            "metrics": result.metrics,
            "artifacts": result.artifacts,
        }
