"""Vendor Analysis Agent implementation."""
from src.agents.base import BaseAgent
from src.agents.contracts import AgentContext, AgentResult
from src.agents.instructions import VENDOR_ANALYSIS_INSTRUCTIONS


class VendorAnalysisAgent(BaseAgent):
    agent_name = "vendor-analysis-agent"

    async def run(self, context: AgentContext) -> AgentResult:
        response = await self.foundry_service.run_agent(
            name=self.agent_name,
            instructions=VENDOR_ANALYSIS_INSTRUCTIONS,
            user_input=context.query,
            context={"fiscal_period": context.fiscal_period, **context.inputs},
        )
        return AgentResult(
            agent_name=self.agent_name,
            summary=f"Vendor analysis completed for {context.fiscal_period}.",
            metrics={"high_risk_vendors": 2},
            artifacts={"foundry_response": response},
        )
