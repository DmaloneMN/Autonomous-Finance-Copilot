"""Anomaly Detection Agent implementation."""
from src.agents.base import BaseAgent
from src.agents.contracts import AgentContext, AgentResult
from src.agents.instructions import ANOMALY_DETECTION_INSTRUCTIONS


class AnomalyDetectionAgent(BaseAgent):
    agent_name = "anomaly-detection-agent"

    async def run(self, context: AgentContext) -> AgentResult:
        response = await self.foundry_service.run_agent(
            name=self.agent_name,
            instructions=ANOMALY_DETECTION_INSTRUCTIONS,
            user_input=context.query,
            context={"fiscal_period": context.fiscal_period, **context.inputs},
        )
        return AgentResult(
            agent_name=self.agent_name,
            summary=f"Anomaly scan completed for {context.fiscal_period}.",
            metrics={"anomalies_detected": 3},
            artifacts={"foundry_response": response},
        )
