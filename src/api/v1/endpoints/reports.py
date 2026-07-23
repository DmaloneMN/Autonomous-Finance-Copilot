"""Executive summary endpoint."""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ReportRequest(BaseModel):
    fiscal_period: str
    audience: str = "CFO"


@router.post("/executive-summary")
async def executive_summary(request: ReportRequest) -> dict[str, str]:
    return {
        "fiscal_period": request.fiscal_period,
        "audience": request.audience,
        "status": "queued",
    }
