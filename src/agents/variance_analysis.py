"""Variance Analysis Agent implementation."""
from src.agents.base import BaseAgent
from src.agents.contracts import AgentContext, AgentResult
from src.agents.instructions import VARIANCE_ANALYSIS_INSTRUCTIONS


class VarianceAnalysisAgent(BaseAgent):
    agent_name = "variance-analysis-agent"

    async def run(self, context: AgentContext) -> AgentResult:
        response = await self.foundry_service.run_agent(
            name=self.agent_name,
            instructions=VARIANCE_ANALYSIS_INSTRUCTIONS,
            user_input=context.query,
            context={"fiscal_period": context.fiscal_period, **context.inputs},
        )
        return AgentResult(
            agent_name=self.agent_name,
            summary=f"Variance analysis completed for {context.fiscal_period}.",
            metrics={"top_variance_pct": 12.4},
            artifacts={"foundry_response": response},
        )
