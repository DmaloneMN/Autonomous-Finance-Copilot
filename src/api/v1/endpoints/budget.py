"""Budget analysis endpoint."""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class BudgetRequest(BaseModel):
    fiscal_period: str
    department: str | None = None


@router.post("/analyze")
async def budget_analysis(request: BudgetRequest) -> dict[str, str | None]:
    return {
        "fiscal_period": request.fiscal_period,
        "department": request.department,
        "status": "queued",
    }
