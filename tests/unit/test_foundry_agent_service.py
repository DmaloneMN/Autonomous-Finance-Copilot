from src.services.foundry_agent_service import FoundryAgentService


class _FakeFoundryAgentService(FoundryAgentService):
    def __init__(self) -> None:
        pass


async def test_foundry_agent_service_returns_completed_response() -> None:
    service = _FakeFoundryAgentService()
    result = await service.run_agent(
        name="budget-agent",
        instructions="Analyze budget performance",
        user_input="Summarize spend variance",
        context={"fiscal_period": "2026-Q1"},
    )
    assert result["agent"] == "budget-agent"
    assert result["status"] == "completed"
    assert "response" in result
