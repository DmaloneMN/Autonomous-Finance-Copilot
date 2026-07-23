"""Unit tests for src/evaluation/scorer.py."""
from __future__ import annotations

import pytest

from src.agents.contracts import AgentResult
from src.evaluation.scorer import EvaluationScorer


@pytest.fixture()
def scorer() -> EvaluationScorer:
    return EvaluationScorer()


async def test_score_empty_list_raises(scorer: EvaluationScorer) -> None:
    """score() with an empty list raises ZeroDivisionError (division by agent count)."""
    with pytest.raises(ZeroDivisionError):
        scorer.score([])


async def test_score_single_result_default_confidence(scorer: EvaluationScorer) -> None:
    """Single AgentResult with no explicit confidence uses the default (0.85)."""
    result = AgentResult(agent_name="budget-agent", summary="ok")
    scores = scorer.score([result])
    assert scores["agent_count"] == 1
    assert scores["completeness_score"] == round(1 / 6, 2)
    assert scores["confidence_score"] == 0.85


async def test_score_multiple_results_mixed_confidence(scorer: EvaluationScorer) -> None:
    """Multiple results: completeness and confidence are computed correctly."""
    results = [
        AgentResult(
            agent_name="budget-agent",
            summary="budget ok",
            metrics={"narrative_confidence": 0.9},
        ),
        AgentResult(
            agent_name="forecast-agent",
            summary="forecast ok",
            metrics={"narrative_confidence": 0.7},
        ),
        AgentResult(
            agent_name="vendor-agent",
            summary="vendor ok",
            metrics={"narrative_confidence": 0.8},
        ),
    ]
    scores = scorer.score(results)
    assert scores["agent_count"] == 3
    assert scores["completeness_score"] == round(3 / 6, 2)
    expected_confidence = round((0.9 + 0.7 + 0.8) / 3, 2)
    assert scores["confidence_score"] == expected_confidence


async def test_completeness_score_formula(scorer: EvaluationScorer) -> None:
    """completeness_score == round(agent_count / 6, 2) for several counts."""
    for count in range(1, 7):
        results = [
            AgentResult(agent_name=f"agent-{i}", summary="ok") for i in range(count)
        ]
        scores = scorer.score(results)
        assert scores["completeness_score"] == round(count / 6, 2)
