"""Simple evaluation scorer for orchestrated agent runs."""
from __future__ import annotations

from src.agents.contracts import AgentResult


class EvaluationScorer:
    def score(self, results: list[AgentResult]) -> dict[str, float | int]:
        completeness = len(results)
        confidence = round(
            sum(float(result.metrics.get("narrative_confidence", 0.85)) for result in results) / len(results),
            2,
        )
        return {
            "agent_count": completeness,
            "completeness_score": round(completeness / 6, 2),
            "confidence_score": confidence,
        }
