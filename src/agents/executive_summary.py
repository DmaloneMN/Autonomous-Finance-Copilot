"""Executive Summary Agent implementation."""
from src.agents.base import BaseAgent
from src.agents.contracts import AgentContext, AgentResult
from src.agents.instructions import EXECUTIVE_SUMMARY_INSTRUCTIONS


class ExecutiveSummaryAgent(BaseAgent):
    agent_name = "executive-summary-agent"

    async def run(self, context: AgentContext) -> AgentResult:
        response = await self.foundry_service.run_agent(
            name=self.agent_name,
            instructions=EXECUTIVE_SUMMARY_INSTRUCTIONS,
            user_input=context.query,
            context={"fiscal_period": context.fiscal_period, **context.inputs},
        )
        return AgentResult(
            agent_name=self.agent_name,
            summary=f"Executive summary prepared for {context.fiscal_period}.",
            metrics={"narrative_confidence": 0.92},
            artifacts={"foundry_response": response},
        )
