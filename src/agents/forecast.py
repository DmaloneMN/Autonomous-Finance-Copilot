"""Forecast Agent implementation."""
from src.agents.base import BaseAgent
from src.agents.contracts import AgentContext, AgentResult
from src.agents.instructions import FORECAST_INSTRUCTIONS


class ForecastAgent(BaseAgent):
    agent_name = "forecast-agent"

    async def run(self, context: AgentContext) -> AgentResult:
        response = await self.foundry_service.run_agent(
            name=self.agent_name,
            instructions=FORECAST_INSTRUCTIONS,
            user_input=context.query,
            context={"fiscal_period": context.fiscal_period, **context.inputs},
        )
        return AgentResult(
            agent_name=self.agent_name,
            summary=f"Forecast generated for {context.fiscal_period}.",
            metrics={"forecast_margin_pct": 31.7},
            artifacts={"foundry_response": response},
        )
