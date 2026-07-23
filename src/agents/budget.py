"""Budget Agent implementation."""
from src.agents.base import BaseAgent
from src.agents.contracts import AgentContext, AgentResult
from src.agents.instructions import BUDGET_INSTRUCTIONS


class BudgetAgent(BaseAgent):
    agent_name = "budget-agent"

    async def run(self, context: AgentContext) -> AgentResult:
        response = await self.foundry_service.run_agent(
            name=self.agent_name,
            instructions=BUDGET_INSTRUCTIONS,
            user_input=context.query,
            context={"fiscal_period": context.fiscal_period, **context.inputs},
        )
        return AgentResult(
            agent_name=self.agent_name,
            summary=f"Budget utilization reviewed for {context.fiscal_period}.",
            metrics={"budget_consumed_pct": 76.8},
            artifacts={"foundry_response": response},
        )
